import sqlite3
import random 


#  Create connection to existing database 
conn = sqlite3.connect("library.db")

cur = conn.cursor()
cur.execute("PRAGMA foreign_keys = ON;")

#  Create authors table 
cur.execute("""
            CREATE TABLE IF NOT EXISTS authors(
            author_id INTEGER PRIMARY KEY, 
            name TEXT,
            country TEXT
);
""")

# Generate Ids function

def author_id(existing_ids):
    while True:
        new_id = random.randint(10000, 99999)
        if new_id not in existing_ids:
            return new_id
        
cur.execute("SELECT author_id FROM authors")
existing_ids = {row[0] for row in cur.fetchall()} # Defines existing_ids as a set 


#  Insert author data
raw_authors = [ 
    ("Toni Morrison", "USA"), 
    ("Robert Greene", "USA"),
    ("Ryan Holiday", "USA"),
    ("James Clear", "USA"),
    ("Borja Villaseca", "SPA"),
    ("Robert Kiyosaki", "USA"),
    ("J.K Rowling", "GBR"),
    ("Joe Dispenza", "USA"),
    ("Tony Robbins", "USA"),
    ("Ernest Hemingway", "USA")
]

def build_authors(raw_authors, existing_ids):
    authors = []
    for name, country in raw_authors:
        cur.execute("SELECT author_id FROM authors WHERE name = ? AND country = ?", (name,country))
        if cur.fetchone() is None:
            id_ = author_id(existing_ids)
            authors.append((id_, name, country))
    return authors

authors = build_authors(raw_authors, existing_ids)

cur.executemany("INSERT OR REPLACE INTO authors (author_id, name, country) VALUES (?, ?, ?)", authors)

#  Fetch data and print
cur.execute("""
            SELECT * FROM authors
            """)


conn.commit()
print(cur.fetchall())
