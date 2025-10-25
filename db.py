import sqlite3 

# 1 Create connection to existing database 
conn = sqlite3.connect("library.db") 

# 2  Create a cursor
cur = conn.cursor() 



# 6 Create books table

cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY,
            author_id INTEGER,
            title TEXT,
            year_published INTEGER,   
            genre TEXT,
            FOREIGN KEY author_id REFERENCES authors(author_id));
            """
            )

books = [
    ("1", "The Art of Seduction", "2001", "Psychology"),
    ("1", "The 48 Laws Of Power", "1998", "Philosophy"),
    ("3", "The Obstacle Is The Way", "2014", "Self-help"),
    ("3", "Ego Is The Enemy", "2016", "Self-help")

]

cur.executemany("INSERT INTO books (author_id, title, year_published, genre) VALUES ( ?, ?, ?, ?)",  books)


cur.execute("SELECT * FROM books")
print(cur.fetchall())