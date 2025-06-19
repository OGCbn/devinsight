import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "devinsight.db")

#this function will create the data tables to hold
#all the info being fed in from from the GIT API
def create_tables():
    conn = sqlite3.connect(DB_PATH)
    #create a cursor object, which is used to execute SQL queries and fetch results from database
    cur = conn.cursor()
    
    ###create the needed tables###
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS repos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT UNIQUE,
        user_id INTEGER REFERENCES users(id)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS commits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sha TEXT UNIQUE,
        message TEXT,
        author TEXT,
        date TEXT,
        repo_id INTEGER REFERENCES repos(id)
    );
    """)

    #save the changes
    conn.commit()
    #disconnect connection
    cur.close()
    conn.close()

