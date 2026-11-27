# ============================================================
# SMART EXPENSE SPLITTER  (Streamlit + SQLite)  - Version 2
# Run with:  python -m streamlit run app.py
# NEW: delete member, delete expense, animations
# ============================================================

import sqlite3
from datetime import date

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Smart Expense Splitter", page_icon="💸")

# ------------------------------------------------------------
# ANIMATION: a smooth fade-in when the page loads / changes
# ------------------------------------------------------------
st.markdown("""
<style>
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(12px);}
    to   {opacity: 1; transform: translateY(0);}
}
.block-container {animation: fadeIn 0.7s ease-in;}

/* Colourful gradient title */
.stApp h1 {
    background: linear-gradient(90deg, #7c5cff, #22d3ee);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    -webkit-text-fill-color: transparent;
}

/* Colourful gradient page background */
.stApp {
    background: linear-gradient(135deg, #fdf4ff 0%, #e0f2fe 50%, #fef9c3 100%);
}

/* Colourful sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ede9fe 0%, #fce7f3 100%);
}

/* Bright gradient buttons that lift and glow on hover */
div.stButton > button {
    background: linear-gradient(90deg, #7c5cff, #ec4899);
    border: none;
    border-radius: 12px;
    padding: 0.5rem 1.2rem;
    transition: all 0.2s ease;
}
div.stButton > button p {
    color: white;
    font-weight: 600;
}
div.stButton > button:hover {
    transform: translateY(-3px) scale(1.03);
    box-shadow: 0 6px 18px rgba(236, 72, 153, 0.45);
}

/* Selected tab in a bright colour */
button[data-baseweb="tab"][aria-selected="true"] {
    color: #7c5cff;
}
</style>
""", unsafe_allow_html=True)

# Show a small pop-up message (toast) saved before a page refresh
if "toast" in st.session_state:
    st.toast(st.session_state.pop("toast"))

# ------------------------------------------------------------
# PART 1: DATABASE
# ------------------------------------------------------------
conn = sqlite3.connect("expenses.db", check_same_thread=False)


def run(query, params=()):
    """Run a command that CHANGES data (INSERT, DELETE...)."""
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    return cur.lastrowid


def fetch(query, params=()):
    """Run a command that READS data (SELECT). Returns a list of rows."""
    cur = conn.cursor()
    cur.execute(query, params)
    return cur.fetchall()


run("""CREATE TABLE IF NOT EXISTS groups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL)""")

run("""CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_id INTEGER NOT NULL,
        name TEXT NOT NULL)""")

run("""CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_id INTEGER NOT NULL,
        payer_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        description TEXT,
        category TEXT,
        date TEXT)""")

run("""CREATE TABLE IF NOT EXISTS splits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        expense_id INTEGER NOT NULL,
        member_id INTEGER NOT NULL,
        share_amount REAL NOT NULL)""")


# ------------------------------------------------------------
# PART 2: LOGIC
# ------------------------------------------------------------
def get_balances(group_id):
    """balance = money they PAID - money they OWE (their shares)."""
    balances = {}
    for mid, name in fetch("SELECT id, name FROM members WHERE group_id=?", (group_id,)):
        paid = fetch("SELECT COALESCE(SUM(amount),0) FROM expenses "
                     "WHERE group_id=? AND payer_id=?", (group_id, mid))[0][0]
        owed = fetch("SELECT COALESCE(SUM(s.share_amount),0) FROM splits s "
                     "JOIN expenses e ON s.expense_id = e.id "
                     "WHERE e.group_id=? AND s.member_id=?", (group_id, mid))[0][0]
        balances[name] = round(paid - owed, 2)
    return balances


def settle(balances):
    """MINIMUM PAYMENTS: match the biggest debtor with the biggest creditor."""
    creditors = [[n, b] for n, b in balances.items() if b > 0.01]
    debtors = [[n, -b] for n, b in balances.items() if b < -0.01]
    payments = []
    while creditors and debtors:
        creditors.sort(key=lambda x: x[1], reverse=True)
        debtors.sort(key=lambda x: x[1], reverse=True)
        c, d = creditors[0], debtors[0]
        amount = round(min(c[1], d[1]), 2)
        payments.append((d[0], c[0], amount))
        c[1] = round(c[1] - amount, 2)
        d[1] = round(d[1] - amount, 2)
        if c[1] <= 0.01:
            creditors.pop(0)
        if d[1] <= 0.01:
            debtors.pop(0)
    return payments


def member_is_used(group_id, member_id):
    """True if this member paid for or shares any expense."""
    paid = fetch("SELECT COUNT(*) FROM expenses WHERE group_id=? AND payer_id=?",
                 (group_id, member_id))[0][0]
    shared = fetch("SELECT COUNT(*) FROM splits s JOIN expenses e ON s.expense_id = e.id "
                   "WHERE e.group_id=? AND s.member_id=?", (group_id, member_id))[0][0]
    return paid > 0 or shared > 0


# ------------------------------------------------------------
# PART 3: SIDEBAR - create / choose / delete a group
# ------------------------------------------------------------
st.title("Smart Expense Splitter")

st.sidebar.header("Groups")
new_group = st.sidebar.text_input("New group name (e.g. Goa Trip)")
if st.sidebar.button("Create group"):
    if new_group.strip():
        run("INSERT INTO groups (name) VALUES (?)", (new_group.strip(),))
        st.session_state["toast"] = "Group created! 🎉"
        st.rerun()
    else:
        st.sidebar.error("Enter a name first.")

groups = fetch("SELECT id, name FROM groups")
if not groups:
    st.info("👈 Create your first group in the sidebar to begin.")
    st.stop()

group_names = {name: gid for gid, name in groups}
chosen = st.sidebar.selectbox("Select group", list(group_names.keys()))
gid = group_names[chosen]

# --- Delete the whole group (trip) ---
with st.sidebar.expander("🗑️ Delete this group"):
    st.warning("This removes the group, its members and ALL its expenses.")
    confirm = st.checkbox("Yes, delete everything in this group")
    if st.button("Delete group"):
        if confirm:
            run("DELETE FROM splits WHERE expense_id IN "
                "(SELECT id FROM expenses WHERE group_id=?)", (gid,))
            run("DELETE FROM expenses WHERE group_id=?", (gid,))
            run("DELETE FROM members WHERE group_id=?", (gid,))
            run("DELETE FROM groups WHERE id=?", (gid,))
            st.session_state["toast"] = f"Group '{chosen}' deleted."
            st.rerun()
        else:
            st.error("Tick the box first to confirm.")

members = fetch("SELECT id, name FROM members WHERE group_id=?", (gid,))
member_ids = {name: mid for mid, name in members}   # name -> id

st.subheader(f"Group: {chosen}")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["👥 Members", "➕ Add Expense", "⚖️ Balances & Settle", "📜 History", "📊 Charts"])

# ------------------------------------------------------------
# TAB 1: MEMBERS (add + delete)
# ------------------------------------------------------------
with tab1:
    new_member = st.text_input("Member name", key="member_name")
    if st.button("Add member"):
        if new_member.strip() and new_member.strip() not in member_ids:
            run("INSERT INTO members (group_id, name) VALUES (?, ?)",
                (gid, new_member.strip()))
            st.session_state["toast"] = f"{new_member.strip()} added! 👋"
            st.rerun()
        else:
            st.error("Enter a new, unique name.")

    st.write("**Current members:**", ", ".join(member_ids.keys()) or "none yet")

    # --- Delete a member ---
    if member_ids:
        st.divider()
        st.write("**Remove a member**")
        to_delete = st.selectbox("Choose member", list(member_ids.keys()), key="del_member")
        if st.button("🗑️ Delete member"):
            if member_is_used(gid, member_ids[to_delete]):
                st.error(f"{to_delete} is part of some expenses. "
                         "Delete those expenses first (History tab), then remove the member.")
            else:
                run("DELETE FROM members WHERE id=?", (member_ids[to_delete],))
                st.session_state["toast"] = f"{to_delete} removed."
                st.rerun()

# ------------------------------------------------------------
# TAB 2: ADD EXPENSE
# ------------------------------------------------------------
with tab2:
    if len(member_ids) < 2:
        st.warning("Add at least 2 members first (Members tab).")
    else:
        names = list(member_ids.keys())
        desc = st.text_input("Description (e.g. Dinner)", key="desc")
        amount = st.number_input("Amount (₹)", min_value=0.0, step=10.0, key="amount")
        category = st.selectbox("Category",
                                ["Food", "Travel", "Rent", "Groceries", "Shopping", "Other"])
        exp_date = st.date_input("Date", value=date.today())
        payer = st.selectbox("Who paid?", names)
        split_type = st.radio("How to split?", ["Equal", "Custom"], horizontal=True)

        shares = {}   # name -> how much that person owes for this expense

        if split_type == "Equal":
            people = st.multiselect("Split between", names, default=names)
            if people and amount > 0:
                each = round(amount / len(people), 2)
                shares = {p: each for p in people}
                diff = round(amount - sum(shares.values()), 2)
                shares[people[0]] = round(shares[people[0]] + diff, 2)
                st.caption(f"Each person pays about ₹{each}")
        else:
            st.write("Enter how much each person owes:")
            for n in names:
                v = st.number_input(f"{n}", min_value=0.0, step=10.0, key=f"custom_{gid}_{n}")
                if v > 0:
                    shares[n] = v
            total = round(sum(shares.values()), 2)
            st.caption(f"Entered total: ₹{total} / Expense amount: ₹{amount}")

        if st.button("Save expense"):
            if amount <= 0 or not shares:
                st.error("Enter an amount and who shares it.")
            elif abs(sum(shares.values()) - amount) > 0.01:
                st.error("Shares must add up to the total amount!")
            else:
                eid = run("INSERT INTO expenses (group_id, payer_id, amount, description, "
                          "category, date) VALUES (?,?,?,?,?,?)",
                          (gid, member_ids[payer], amount, desc, category, str(exp_date)))
                for person, share in shares.items():
                    run("INSERT INTO splits (expense_id, member_id, share_amount) "
                        "VALUES (?,?,?)", (eid, member_ids[person], share))
                st.success("Expense saved!")
                st.balloons()   # ANIMATION: balloons float up when an expense is saved

# ------------------------------------------------------------
# TAB 3: BALANCES & SETTLEMENT
# ------------------------------------------------------------
with tab3:
    balances = get_balances(gid)
    if not balances:
        st.info("No members yet.")
    else:
        st.write("**Each member's balance** (+ gets money, − owes money)")
        st.dataframe(pd.DataFrame({"Member": list(balances.keys()),
                                   "Balance (₹)": list(balances.values())}),
                     hide_index=True)

        st.write("**Who owes whom (minimum payments):**")
        payments = settle(balances)
        if not payments:
            st.success("All settled! Nobody owes anything. 🎉")
        for payer_n, receiver_n, amt in payments:
            st.write(f"👉 **{payer_n}** pays **{receiver_n}** ₹{amt:.2f}")

# ------------------------------------------------------------
# TAB 4: EXPENSE HISTORY (+ delete expense)
# ------------------------------------------------------------
with tab4:
    rows = fetch("SELECT e.id, e.date, e.description, e.category, m.name, e.amount "
                 "FROM expenses e JOIN members m ON e.payer_id = m.id "
                 "WHERE e.group_id=? ORDER BY e.date DESC, e.id DESC", (gid,))
    if not rows:
        st.info("No expenses yet.")
    else:
        df = pd.DataFrame(rows, columns=["ID", "Date", "Description", "Category",
                                         "Paid by", "Amount (₹)"])
        st.dataframe(df, hide_index=True)

        st.divider()
        st.write("**Delete an expense**")
        labels = {f"#{r[0]} | {r[1]} | {r[2]} | ₹{r[5]} (paid by {r[4]})": r[0] for r in rows}
        pick = st.selectbox("Choose expense", list(labels.keys()), key="del_expense")
        if st.button("🗑️ Delete expense"):
            run("DELETE FROM splits WHERE expense_id=?", (labels[pick],))
            run("DELETE FROM expenses WHERE id=? AND group_id=?", (labels[pick], gid))
            st.session_state["toast"] = "Expense deleted."
            st.rerun()

# ------------------------------------------------------------
# TAB 5: CHARTS
# ------------------------------------------------------------
with tab5:
    cat_rows = fetch("SELECT category, SUM(amount) FROM expenses WHERE group_id=? "
                     "GROUP BY category", (gid,))
    if not cat_rows:
        st.info("Add expenses to see charts.")
    else:
        st.write("**Spending by category**")
        st.bar_chart(pd.DataFrame(cat_rows, columns=["Category", "Total"]).set_index("Category"))

        month_rows = fetch("SELECT substr(date,1,7), SUM(amount) FROM expenses "
                           "WHERE group_id=? GROUP BY substr(date,1,7) ORDER BY 1", (gid,))
        st.write("**Monthly report**")
        st.bar_chart(pd.DataFrame(month_rows, columns=["Month", "Total"]).set_index("Month"))
