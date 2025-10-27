import streamlit as st
import sqlite3
import pandas as pd 

DB = "library.db"

# ------- Database Connection -------

def get_conn():
    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

# ------- Sidebar Navigation -------

st.sidebar.title("📚 Library Database")
menu = ["Run SQL", "View Tables", "Insert Data", "Update Data", "Delete Data"]
choice = st.sidebar.radio("Select Mode", menu)

# ------- SQL Query Executor -------

if choice == "Run SQL":
    st.title("SQL Workbench Mode")
    query = st.text_area("Enter SQL query:")
    if st.button("Execute"):
        try:
            conn = get_conn()
            result = pd.read_sql_query(query, conn)
            st.dataframe(result)
            conn.commit()
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            conn.close()

# ------- View Tables -------

elif choice == "View Tables":
    st.title("Browse Database")
    conn = get_conn()
    tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
    table_choice = st.selectbox("Select a Table", tables["name"].tolist())
    df = pd.read_sql(f"SELECT * FROM {table_choice}", conn)
    st.dataframe(df)
    conn.close()

# ------- Insert Data -------

elif choice == "Insert Data":
    st.title("+ Insert New Record")
    table = st.selectbox("Table", ["authors", "books", "loans"])

    conn = get_conn()

    if table == "authors":
        with st.form("add_author"):
            name = st.text_input("Name")
            country = st.text_input("Country")
            submit = st.form_submit_button("Insert Author")
            if submit:
                conn.execute("INSERT OR REPLACE INTO authors (name, country) VALUES (?, ?)",(name, country))
                conn.commit()
                st.success(f"Author {name} added successfully!")

    if table == "books":
        with st.form("add_book"):
            title = st.text_input("Title")
            genre = st.text_input("Genre")
            year = st.number_input("Year Published", step=1)
            author_id = st.number_input("Author ID", step=1)
            submit = st.form_submit_button("Insert Book")
            if submit:
                conn.execute("INSERT OR REPLACE INTO books (title, genre, published_year, author_id) VALUES (?, ?, ?, ?)",(title, genre, year, author_id))
                conn.commit()
                st.success(f"Book {title} successfully added!")

    if table == "loans":
        with st.form("add_loans"):
            book_id = st.number_input("Book ID", step=1)
            member_id = st.number_input("Member ID", step=1)
            loan_date = st.date_input("Loan Date")
            return_date = st.date_input("Return Date")
            submit = st.form_submit_button("Insert Loan")
            if submit:
                conn.execute("INSERT OR REPLACE INTO loans (book_id, member_id, loan_date, return_date) VALUES (?, ?, ?, ?)", (book_id, member_id, loan_date.isoformat(), return_date.isoformat()))
                conn.commit()
                st.success(f"Loan added successfully!")

elif choice == "Update Data":
    st.title("Update Existing Record")
    table = st.selectbox("Table", ["authors", "books", "loans"])
    conn = get_conn()
    df = pd.read_sql(f"SELECT * FROM {table}", conn)
    st.dataframe(df)
    id_col = table[:-1] + "_id"
    record_id = st.number_input(f"Enter {id_col} to update", step=1)
    column = st.text_input("Column to update")
    new_value = st.text_input("New Value")
    if st.button("Update"):
        try:
            conn.execute(f"UPDATE {table} SET {column}=? WHERE {id_col}=?", (new_value, record_id))
            conn.commit()
            st.success("Record successfully updated!")
        except Exception as e:
            st.error(f"Error: {e}")
    conn.close()

elif choice == "Delete Data":
    st.title("Delete Record")
    table = st.selectbox( "Table", ["authors", "books", "loans"])
    conn = get_conn()
    id_col = table[:-1] + "_id"
    record_id = st.number_input(f"Enter {id_col} to delete", step=1)
    if st.button("Delete"):
        try:
            conn.execute(f"DELETE FROM {table} WHERE {id_col}=?", (record_id))
            conn.commit()
            st.warning("Record deleted successfully!")
        except Exception as e:
            st.error(f"Error: {e}")
    conn.close()