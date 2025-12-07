# 📚 Library Simulation Project (SQLite + Streamlit)

https://library-database-simulation-ny4nyxgvhme4wc5nw35oyz.streamlit.app/

This project is a complete simulation of a small-scale library system built from the ground up using Python, SQLite, and Streamlit. It covers everything from database schema creation and data insertion to building a fully interactive web app.

---

## 🎯 Project Goals

- ✅ Design relational database schema (authors, books, loans)
- ✅ Create and populate SQLite tables using Python (`sqlite3`)
- ✅ Perform SQL queries and manage data with Pandas
- ✅ Build a Streamlit-based CRUD application interface
- ✅ Practice modular design and clean code architecture

---

## 🧱 Database Design

**Entities:**
- `authors`: ID, name, country
- `books`: ID, title, genre, published year, author ID (foreign key)
- `loans`: ID, book ID, member ID, loan date, return date

All tables enforce referential integrity with **foreign key constraints**.

---

## 🖥️ Streamlit App Features

- 🔍 **View Tables**: Browse data in any table
- ➕ **Insert Records**: Add new authors, books, and loans
- ✏️ **Update Records**: Edit fields by specifying the column
- 🗑️ **Delete Records**: Remove rows using primary key IDs
- 🧠 **SQL Workbench**: Run raw SQL queries and view results

---

## 🧪 Tech Stack

- **Python 3**
- **SQLite3**
- **Pandas**
- **Streamlit**

---

## 📁 Project Structure

```bash
.
├── app.py           # Main Streamlit app entrypoint
├── authors.py       # Author form + logic
├── books.py         # Book form + logic
├── loans.py         # Loan form + logic
├── db.py            # DB connection + setup
├── library.db       # SQLite database file (prebuilt)
├── main.ipynb       # Notebook for schema creation + test inserts
├── requirements.txt # App dependencies
├── README.md        # Project documentation
└── .gitignore       # Git ignore rules
