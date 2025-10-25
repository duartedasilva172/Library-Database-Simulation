import sqlite3
import random

# SET UP

conn = sqlite3.connect("library.db")

cur = conn.cursor()
cur.execute("PRAGMA foreign_keys = ON;")
cur.execute("""
            CREATE TABLE IF NOT EXISTS loans(
            loan_id INTEGER PRIMARY KEY,
            book_id INTEGER,
            member_id INTEGER,
            loan_date TEXT,
            return_date TEXT,
            FOREIGN KEY (book_id) REFERENCES books(book_id)
            );
            """)


# Generate Ids

def loans_id(existing_ids):
    while True:
        new_id = random.randint(100000, 999999)
        if new_id not in existing_ids:
            return new_id
        
def member_id(existing_member_id):
    while True:
        new_member = random.randint(1000, 9999)
        if new_member not in existing_member_id:
            return new_member
        
cur.execute("SELECT * FROM loans")
existing_ids = {row[0] for row in cur.fetchall()}
existing_member_id = {row[2] for row in cur.fetchall()}


# INSERT DATA

loans = [
    (loans_id(existing_ids), "14302", member_id(existing_member_id),  "January 23rd 2021", "January 30th, 2021"),
    (loans_id(existing_ids), "14888", member_id(existing_member_id), "January 25th 2021", "January 31st 2021"),
    (loans_id(existing_ids), "18703", member_id(existing_member_id),  "January 26th 2021", "January 28th 2021")
 ]

cur.executemany("INSERT OR REPLACE INTO loans (loan_id, book_id, member_id, loan_date, return_date) VALUES (?, ?, ?, ?, ?)", loans)
cur.execute("SELECT * FROM loans")
print(cur.fetchall())