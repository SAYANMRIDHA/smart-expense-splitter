# Smart Expense Splitter

Hackathon problem: **SW-15 (FinTech / Databases)**

**Live app:** https://smart-expense-splitter-kwxzh2jnzuk7zygpedfnyt.streamlit.app/

## Problem
Roommates and friends share expenses like groceries, rent and cabs.
Tracking who owes whom causes confusion and arguments.

## Our Solution
A web app where a group records shared expenses in a private **room** and sees
exactly who owes how much to whom. Open the link on any phone, on any network.

## USP
**Settle up in the fewest payments.** The app calculates the minimum number of
transfers needed to clear all balances in a room.

## Features
- **Accounts:** register and log in (passwords stored as PBKDF2-SHA256 hashes)
- **Rooms with a code:** the host creates a room and shares a 6-character code; friends join with it
- **Guests:** the host can add friends who have no account
- **Expenses:** payer, amount, category, equal or custom split
- **Balances and who-owes-whom** with the minimum number of payments
- **UPI QR pay:** each user saves a UPI ID and QR; the payer sees it next to each payment
- **Encrypted UPI vault:** UPI IDs and QR images are encrypted before they are saved
- **Bill scan (optional OCR):** fills in the total from a bill photo
- **Charts and history:** category chart, monthly report, expense history with delete
- **Close room:** when everyone is settled the host closes the room. Bills are deleted
  and every member keeps a short summary in **My History**

## Tech Stack
Python, Streamlit, SQLite, Pandas, Altair

## Files
- `app.py` - the screens (Streamlit)
- `logic.py` - database and money logic (tested separately)
- `requirements.txt` - libraries

## How to Run
1. Install Python
2. `pip install -r requirements.txt`
3. `python -m streamlit run app.py`

Optional bill scanning: `pip install rapidocr-onnxruntime` (the app works without it).

## Deploy (Streamlit Community Cloud)
1. Push this repo to GitHub.
2. On share.streamlit.io create an app: branch `main`, main file `app.py`.
3. In the app's **Settings -> Secrets** add `SPLITTER_MASTER_KEY = "any-long-random-text"`
   so encrypted UPI data stays readable after a restart.

## Known limits
- The free cloud server can reset its files when the app restarts, so the online database
  is for demo use. The next step is a managed cloud database.
- Login lasts until the page is refreshed.

## Future Plans
- Cloud database (Amazon RDS / DynamoDB)
- Login with Amazon Cognito
- Bill scanning with Amazon Textract
- One-tap UPI payment links

## Team
- SAYAN
- PIYUSH
- KESAV
- ASUTHOSH
