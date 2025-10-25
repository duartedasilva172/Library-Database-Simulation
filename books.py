import sqlite3 
import random

conn = sqlite3.connect("library.db")

cur = conn.cursor()
cur.execute("PRAGMA foreign_keys = ON;")

cur.execute(""" 
            CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY,
            title TEXT,
            genre TEXT,
            published_year INTEGER,
            author_id INTEGER,
            FOREIGN KEY (author_id) REFERENCES authors(author_id)
        );
""")

# Generate book Ids
def book_id(existing_ids):
    while True:
        new_id = random.randint(10000, 99999)
        if new_id not in existing_ids:
            return new_id
        

cur.execute("SELECT * FROM books")
cur.fetchall()
existing_ids = {row[0] for row in cur.fetchall()}

# Bulding books function

def build_books(raw_books, existing_ids, cur):
    books = []
    for title, genre, year, author_name in raw_books:
        # Look up author_id using author_name
        cur.execute("SELECT author_id FROM authors WHERE name = ?", (author_name))
        result = cur.fetchone()

        if result: # Only insert if author exists
            author_id = result[0]
            id_ = book_id(existing_ids)
            existing_ids.add(id_)
            books.append((id_, title, genre, year, author_id))
        else:
            print(f"Author '{author_name}' not found in databse. Skipping book; {title}")
    return books

# Insert Data

raw_books =  [
    ("Ego Is The Enemy", "Self-Help", "2016", "Ryan Holiday"),
    ("The Old Man & The Sea", "Fiction", "1952", "Ernest Hemingway"),
    ("Men Without Women", "Fiction", "1927", "Ernest Hemingway"),
    ("Stillness Is The Key", "Philosophy, Self_help","2019", "Ryan Holiday"),
    ("Discipline Is Destiny", "Philosphy, Self-Help", "2022", "Ryan Holiday"),
    ("The Obstacle Is The Way", "Philosophy", "2014", "Ryan Holiday"),
    ("Atomic Habits", "Self-Help", "2018", "James Clear"),
    ("Harry Potter & The Philosopher's Stone", "Fiction", "1997", "J.K Rowling"),
    ("Harry Potter & The Chamber Of Secrets", "Fiction", "1998", "J.K Rowling"),
    ("Harry Potter & The Prisoner Of Azkaban", "Fiction", "1999", "J.K Rowling"),
    ("Harry Potter & The Goblet Of Fire", "Fiction", "2002", "J.K Rowling"),
    ("Harry Potter & The Order Of The Phoenix", "Fiction", "2003", "J.K Rowling"),
    ("Harry Potter & The Half-Blood Prince", "Fiction", "2005", "J.K Rowling"),
    ("Harry Potter & The Deathly Hallows", "Fiction", "1997", "J.K Rowling"),
    ("The Art Of Seduction", "Strategy", "2001", "Robert Greene"),
    ("The 48 Laws Of Power", "Stategy, Self-Help", "1998", "Robert Greene"),
    ("Que Harías Si No Tuvieras Miedo", "Self-Help", "2013", "Borja Villaseca"),
    ("Rich Dad Poor Dad", "Finance", "1997", "Robert Kiyosaki"),
    ("Breaking The Habit Of Being Yourself", "Self-Help, Psychology", "2012", "Joe Dispenza"),
    ("Song Of Solomon", "Novel, Fiction", "1977", "Toni Morrison"),
    ("The Bluest Eye", "Novel, Fiction", "1970", "Toni Morrison")
]

books = build_books(raw_books, existing_ids, cur)

cur.executemany("""
            INSERT OR REPLACE INTO books (book_id, title, genre, published_year, author_id)
            VALUES (?, ?, ?, ?, ?)
""", books)

cur.execute("SELECT book_id FROM books")
print(cur.fetchall())

conn.commit()
conn.close()



