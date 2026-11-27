# Smart Expense Splitter

Hackathon problem: SW-15 (FinTech / Databases)

## Problem
Roommates and friends share expenses like groceries, rent and cabs.
Tracking who owes whom causes confusion and arguments.

## Our Solution
A web app where a group records shared expenses and sees exactly
who owes how much to whom.

## USP
Settle up in the fewest payments. Our app calculates the minimum
number of transfers needed to clear all balances in a group.

## Features
- Create and delete groups, add and remove members
- Add expenses with payer, amount, category and split (equal or custom)
- Balance for each member
- Settlement list with the minimum number of payments
- Expense history with delete option
- Category and monthly spending charts
- All data stored in a SQLite database

## Tech Stack
Python, Streamlit, SQLite, Pandas

## How to Run
1. Install Python
2. pip install -r requirements.txt
3. streamlit run app.py

## Future Plans
- Bill scanning with OCR (Amazon Textract)
- User login (Amazon Cognito)
- Cloud database (Amazon RDS / DynamoDB)

## Team
- SAYAN
- PIYUSH
- KESAV
- ASUTHOSH