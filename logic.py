# ============================================================
# logic.py  -  hardened SQLite database + money logic (v3)
# Pairs directly with the encrypted vibrant app_v2.py
# Zero external pip dependencies.
# ============================================================
import hashlib
import hmac
import os
import re
import secrets
import sqlite3
import threading
from datetime import date

DB_PATH = "splitter_v2.db"
CODE_CHARS = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"   # no confusing 0/O/1/I


# ------------------------------------------------------------
# DATABASE SETUP
# ------------------------------------------------------------
class _LockedConn:
    """Streamlit serves every visitor in its own thread but the app shares ONE database
    connection. This wrapper makes each database call wait its turn (a lock), so two
    people tapping buttons at the same moment cannot corrupt each other's work."""

    def __init__(self, raw):
        self._raw = raw
        self._lock = threading.RLock()

    def execute(self, *args, **kwargs):
        with self._lock:
            return self._raw.execute(*args, **kwargs)

    def executescript(self, *args, **kwargs):
        with self._lock:
            return self._raw.executescript(*args, **kwargs)

    def commit(self):
        with self._lock:
            return self._raw.commit()

    def rollback(self):
        with self._lock:
            return self._raw.rollback()

    def __getattr__(self, name):          # anything else goes straight to the real connection
        return getattr(self._raw, name)


def connect(path=DB_PATH):
    raw = sqlite3.connect(path, check_same_thread=False, timeout=15.0)
    raw.row_factory = sqlite3.Row
    try:
        raw.execute("PRAGMA journal_mode=WAL;")
        raw.execute("PRAGMA synchronous=NORMAL;")
    except sqlite3.DatabaseError:
        pass
    conn = _LockedConn(raw)
    init_db(conn)
    return conn


def init_db(conn):
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        display_name TEXT NOT NULL,
        salt TEXT NOT NULL,
        pw_hash TEXT NOT NULL,
        upi_id TEXT DEFAULT '',
        qr_image BLOB,
        avatar_image BLOB);

    CREATE TABLE IF NOT EXISTS rooms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        code TEXT UNIQUE NOT NULL,
        host_user_id INTEGER NOT NULL,
        created_on TEXT);

    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_id INTEGER NOT NULL,
        user_id INTEGER,            -- NULL = guest without an account
        name TEXT NOT NULL);

    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_id INTEGER NOT NULL,
        payer_id INTEGER NOT NULL,  -- members.id
        amount REAL NOT NULL,
        description TEXT,
        category TEXT,
        date TEXT);

    CREATE TABLE IF NOT EXISTS splits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        expense_id INTEGER NOT NULL,
        member_id INTEGER NOT NULL,
        share_amount REAL NOT NULL);

    CREATE TABLE IF NOT EXISTS settlements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_id INTEGER NOT NULL,
        from_member INTEGER NOT NULL,
        to_member INTEGER NOT NULL,
        amount REAL NOT NULL,
        date TEXT);

    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        room_name TEXT,
        host_name TEXT,
        members_text TEXT,
        total_spent REAL,
        my_paid REAL,
        my_share REAL,
        expense_count INTEGER,
        closed_on TEXT);
    """)
    user_columns = {row["name"] for row in conn.execute("PRAGMA table_info(users)")}
    if "avatar_image" not in user_columns:
        conn.execute("ALTER TABLE users ADD COLUMN avatar_image BLOB")
    conn.commit()


def _one(conn, q, p=()):
    r = conn.execute(q, p).fetchone()
    return dict(r) if r else None


def _all(conn, q, p=()):
    return [dict(r) for r in conn.execute(q, p).fetchall()]


# ------------------------------------------------------------
# USERS / LOGIN
# ------------------------------------------------------------
def _hash(password, salt_hex):
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt_hex),
        100_000,
    ).hex()


def create_user(conn, username, display_name, password):
    username = username.strip().lower()
    display_name = display_name.strip()
    if len(username) < 3:
        return False, "Username must be at least 3 characters."
    if not display_name:
        return False, "Enter your name."
    if len(password) < 4:
        return False, "Password must be at least 4 characters."
    if _one(conn, "SELECT id FROM users WHERE username=?", (username,)):
        return False, "That username is already taken."
    salt = os.urandom(16).hex()
    conn.execute(
        "INSERT INTO users (username, display_name, salt, pw_hash) VALUES (?,?,?,?)",
        (username, display_name, salt, _hash(password, salt)),
    )
    conn.commit()
    return True, "Account created! You can log in now."


def check_login(conn, username, password):
    u = _one(conn, "SELECT * FROM users WHERE username=?", (username.strip().lower(),))
    if u and hmac.compare_digest(_hash(password, u["salt"]), u["pw_hash"]):
        return u
    return None


def get_user(conn, uid):
    return _one(conn, "SELECT * FROM users WHERE id=?", (uid,))


def update_profile(conn, uid, display_name, upi_id):
    clean_name = display_name.strip()
    clean_upi = (upi_id or "").strip()
    conn.execute(
        "UPDATE users SET display_name=?, upi_id=? WHERE id=?",
        (clean_name, clean_upi, uid),
    )
    # Keep active room member names synced unless another member already has that name
    for row in _all(conn, "SELECT id, room_id FROM members WHERE user_id=?", (uid,)):
        clash = _one(
            conn,
            "SELECT id FROM members WHERE room_id=? AND lower(name)=lower(?) AND id!=?",
            (row["room_id"], clean_name, row["id"]),
        )
        if not clash:
            conn.execute("UPDATE members SET name=? WHERE id=?", (clean_name, row["id"]))
    conn.commit()


def set_qr(conn, uid, blob):
    payload = sqlite3.Binary(blob) if blob is not None else None
    conn.execute("UPDATE users SET qr_image=? WHERE id=?", (payload, uid))
    conn.commit()


def set_avatar(conn, uid, blob):
    payload = sqlite3.Binary(blob) if blob is not None else None
    conn.execute("UPDATE users SET avatar_image=? WHERE id=?", (payload, uid))
    conn.commit()


# ------------------------------------------------------------
# ROOMS
# ------------------------------------------------------------
def _new_code(conn):
    while True:
        code = "".join(secrets.choice(CODE_CHARS) for _ in range(6))
        if not _one(conn, "SELECT id FROM rooms WHERE code=?", (code,)):
            return code


def create_room(conn, name, host_uid):
    host = get_user(conn, host_uid)
    cur = conn.execute(
        "INSERT INTO rooms (name, code, host_user_id, created_on) VALUES (?,?,?,?)",
        (name.strip(), _new_code(conn), host_uid, str(date.today())),
    )
    rid = cur.lastrowid
    conn.execute(
        "INSERT INTO members (room_id, user_id, name) VALUES (?,?,?)",
        (rid, host_uid, host["display_name"]),
    )
    conn.commit()
    return rid


def join_room(conn, code, uid):
    room = _one(conn, "SELECT * FROM rooms WHERE code=?", (code.strip().upper(),))
    if not room:
        return False, "No room found with that code.", None
    if _one(conn, "SELECT id FROM members WHERE room_id=? AND user_id=?", (room["id"], uid)):
        return False, "You are already in this room.", room["id"]
    user = get_user(conn, uid)
    name = user["display_name"]
    if _one(conn, "SELECT id FROM members WHERE room_id=? AND lower(name)=lower(?)", (room["id"], name)):
        name = f"{name} ({user['username']})"
    conn.execute(
        "INSERT INTO members (room_id, user_id, name) VALUES (?,?,?)",
        (room["id"], uid, name),
    )
    conn.commit()
    return True, f"Joined '{room['name']}'!", room["id"]


def rooms_for_user(conn, uid):
    return _all(
        conn,
        "SELECT r.* FROM rooms r JOIN members m ON m.room_id = r.id "
        "WHERE m.user_id=? ORDER BY r.id DESC",
        (uid,),
    )


def room_members(conn, rid):
    return _all(
        conn,
        "SELECT m.id, m.user_id, m.name, u.avatar_image "
        "FROM members m LEFT JOIN users u ON m.user_id=u.id "
        "WHERE m.room_id=? ORDER BY m.id",
        (rid,),
    )


def add_guest(conn, rid, name):
    name = name.strip()
    if not name:
        return False
    if _one(conn, "SELECT id FROM members WHERE room_id=? AND lower(name)=lower(?)", (rid, name)):
        return False
    conn.execute("INSERT INTO members (room_id, user_id, name) VALUES (?,NULL,?)", (rid, name))
    conn.commit()
    return True


def member_used(conn, rid, mid):
    a = _one(conn, "SELECT COUNT(*) c FROM expenses WHERE room_id=? AND payer_id=?", (rid, mid))["c"]
    b = _one(
        conn,
        "SELECT COUNT(*) c FROM splits s JOIN expenses e ON s.expense_id=e.id "
        "WHERE e.room_id=? AND s.member_id=?",
        (rid, mid),
    )["c"]
    c = _one(
        conn,
        "SELECT COUNT(*) c FROM settlements WHERE room_id=? AND (from_member=? OR to_member=?)",
        (rid, mid, mid),
    )["c"]
    return (a + b + c) > 0


def remove_member_if_unused(conn, rid, mid):
    if member_used(conn, rid, mid):
        return False
    conn.execute("DELETE FROM members WHERE id=? AND room_id=?", (mid, rid))
    conn.commit()
    return True


def user_of_member(conn, mid):
    return _one(
        conn,
        "SELECT u.* FROM users u JOIN members m ON m.user_id=u.id WHERE m.id=?",
        (mid,),
    )


# ------------------------------------------------------------
# EXPENSES
# ------------------------------------------------------------
def split_equal(amount, mids):
    """Equal split; the first person absorbs any 0.01 rounding difference."""
    if not mids or amount <= 0:
        return {}
    each = round(amount / len(mids), 2)
    shares = {m: each for m in mids}
    shares[mids[0]] = round(shares[mids[0]] + round(amount - each * len(mids), 2), 2)
    return shares


def add_expense(conn, rid, payer_mid, amount, desc, category, date_str, shares):
    amount = round(float(amount), 2)
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    if not shares or abs(sum(shares.values()) - amount) > 0.01:
        raise ValueError("Shares must add up to the amount.")
    cur = conn.execute(
        "INSERT INTO expenses (room_id, payer_id, amount, description, category, date) "
        "VALUES (?,?,?,?,?,?)",
        (rid, payer_mid, amount, (desc or "").strip(), category, date_str),
    )
    eid = cur.lastrowid
    for mid, sh in shares.items():
        if sh > 0:
            conn.execute(
                "INSERT INTO splits (expense_id, member_id, share_amount) VALUES (?,?,?)",
                (eid, mid, round(float(sh), 2)),
            )
    conn.commit()
    return eid


def list_expenses(conn, rid):
    return _all(
        conn,
        "SELECT e.id, e.date, e.description, e.category, m.name AS payer, e.amount "
        "FROM expenses e JOIN members m ON e.payer_id=m.id "
        "WHERE e.room_id=? ORDER BY e.date DESC, e.id DESC",
        (rid,),
    )


def delete_expense(conn, rid, eid):
    conn.execute(
        "DELETE FROM splits WHERE expense_id IN (SELECT id FROM expenses WHERE id=? AND room_id=?)",
        (eid, rid),
    )
    conn.execute("DELETE FROM expenses WHERE id=? AND room_id=?", (eid, rid))
    conn.commit()


def record_payment(conn, rid, from_mid, to_mid, amount):
    amount = round(float(amount), 2)
    if amount <= 0 or from_mid == to_mid:
        return
    conn.execute(
        "INSERT INTO settlements (room_id, from_member, to_member, amount, date) VALUES (?,?,?,?,?)",
        (rid, from_mid, to_mid, amount, str(date.today())),
    )
    conn.commit()


def list_payments(conn, rid):
    return _all(
        conn,
        "SELECT s.date, f.name AS payer, t.name AS receiver, s.amount "
        "FROM settlements s JOIN members f ON s.from_member=f.id "
        "JOIN members t ON s.to_member=t.id WHERE s.room_id=? ORDER BY s.id DESC",
        (rid,),
    )


# ------------------------------------------------------------
# BALANCES + MINIMUM PAYMENTS
# ------------------------------------------------------------
def compute_balances(conn, rid):
    """net = paid - share + payments made - payments received"""
    out = {}
    for m in room_members(conn, rid):
        mid = m["id"]
        paid = _one(
            conn,
            "SELECT COALESCE(SUM(amount),0) v FROM expenses WHERE room_id=? AND payer_id=?",
            (rid, mid),
        )["v"]
        share = _one(
            conn,
            "SELECT COALESCE(SUM(s.share_amount),0) v FROM splits s "
            "JOIN expenses e ON s.expense_id=e.id WHERE e.room_id=? AND s.member_id=?",
            (rid, mid),
        )["v"]
        pay_out = _one(
            conn,
            "SELECT COALESCE(SUM(amount),0) v FROM settlements WHERE room_id=? AND from_member=?",
            (rid, mid),
        )["v"]
        pay_in = _one(
            conn,
            "SELECT COALESCE(SUM(amount),0) v FROM settlements WHERE room_id=? AND to_member=?",
            (rid, mid),
        )["v"]
        out[mid] = {
            "name": m["name"],
            "paid": round(paid, 2),
            "share": round(share, 2),
            "net": round(paid - share + pay_out - pay_in, 2),
        }
    return out


def settle_plan(nets):
    """Greedy min-transfer settlement: repeatedly match largest debtor with largest creditor."""
    creditors = [[m, b] for m, b in nets.items() if b > 0.01]
    debtors = [[m, -b] for m, b in nets.items() if b < -0.01]
    plan = []
    while creditors and debtors:
        creditors.sort(key=lambda x: x[1], reverse=True)
        debtors.sort(key=lambda x: x[1], reverse=True)
        c, d = creditors[0], debtors[0]
        amt = round(min(c[1], d[1]), 2)
        plan.append((d[0], c[0], amt))
        c[1] = round(c[1] - amt, 2)
        d[1] = round(d[1] - amt, 2)
        if c[1] <= 0.01:
            creditors.pop(0)
        if d[1] <= 0.01:
            debtors.pop(0)
    return plan


def category_totals(conn, rid):
    return _all(
        conn,
        "SELECT category, SUM(amount) AS total FROM expenses WHERE room_id=? GROUP BY category",
        (rid,),
    )


def month_totals(conn, rid):
    return _all(
        conn,
        "SELECT substr(date,1,7) AS month, SUM(amount) AS total FROM expenses "
        "WHERE room_id=? GROUP BY substr(date,1,7) ORDER BY 1",
        (rid,),
    )


# ------------------------------------------------------------
# CLOSE ROOM: archive summary for every member, then wipe room rows
# ------------------------------------------------------------
def close_room(conn, rid, host_uid):
    room = _one(conn, "SELECT * FROM rooms WHERE id=?", (rid,))
    if not room:
        return False, "Room not found."
    if room["host_user_id"] != host_uid:
        return False, "Only the host can close the room."
    bal = compute_balances(conn, rid)
    if settle_plan({m: b["net"] for m, b in bal.items()}):
        return False, "Everyone must be settled before closing the room."

    host = get_user(conn, host_uid)
    members = room_members(conn, rid)
    total = _one(conn, "SELECT COALESCE(SUM(amount),0) v FROM expenses WHERE room_id=?", (rid,))["v"]
    count = _one(conn, "SELECT COUNT(*) c FROM expenses WHERE room_id=?", (rid,))["c"]
    names = ", ".join(m["name"] for m in members)

    for m in members:
        if m["user_id"]:
            conn.execute(
                "INSERT INTO history (user_id, room_name, host_name, members_text, total_spent, "
                "my_paid, my_share, expense_count, closed_on) VALUES (?,?,?,?,?,?,?,?,?)",
                (
                    m["user_id"],
                    room["name"],
                    host["display_name"],
                    names,
                    round(total, 2),
                    bal[m["id"]]["paid"],
                    bal[m["id"]]["share"],
                    count,
                    str(date.today()),
                ),
            )

    conn.execute("DELETE FROM splits WHERE expense_id IN (SELECT id FROM expenses WHERE room_id=?)", (rid,))
    conn.execute("DELETE FROM expenses WHERE room_id=?", (rid,))
    conn.execute("DELETE FROM settlements WHERE room_id=?", (rid,))
    conn.execute("DELETE FROM members WHERE room_id=?", (rid,))
    conn.execute("DELETE FROM rooms WHERE id=?", (rid,))
    conn.commit()
    return True, "Room closed. A short history was saved to every member's account."


def history_for_user(conn, uid):
    return _all(
        conn,
        "SELECT closed_on, room_name, host_name, members_text, total_spent, my_paid, my_share, "
        "expense_count FROM history WHERE user_id=? ORDER BY id DESC",
        (uid,),
    )


# ------------------------------------------------------------
# BILL SCAN HELPER: extract total amount from OCR text lines
# ------------------------------------------------------------
_NUM = re.compile(r"\d{1,3}(?:,\d{2,3})+(?:\.\d{1,2})?|\d+(?:\.\d{1,2})?")


def _numbers(text):
    vals = []
    for tok in _NUM.findall(text):
        try:
            v = float(tok.replace(",", ""))
        except ValueError:
            continue
        if 1 <= v <= 1_000_000:
            vals.append(v)
    return vals


def parse_total(lines):
    key = re.compile(r"total|amount|net|payable|due", re.I)
    skip = re.compile(r"sub\s*-?\s*total|tax|gst|cgst|sgst|discount|change|tendered|cash", re.I)
    candidates = []
    for i, line in enumerate(lines):
        if key.search(line) and not skip.search(line):
            candidates += _numbers(line)
            if i + 1 < len(lines) and not _numbers(line):
                candidates += _numbers(lines[i + 1])
    if candidates:
        return max(candidates)
    allnums = [v for line in lines for v in _numbers(line)]
    return max(allnums) if allnums else None