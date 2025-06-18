import os
import psycopg2
from dotenv import load_dotenv

#load data from .env
load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

#this function will create the data tables to hold
#all the info being fed in from from the GIT API
def create_tables():
    conn = psycopg2.connect(DB_URL)
    #create a cursor object, which is used to execute SQL queries and fetch results from database
    cur = conn.cursor()
    
    ###create the needed tables###
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS repos (
        id SERIAL PRIMARY KEY,
        full_name TEXT UNIQUE,
        user_id INTEGER REFERENCES users(id)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS commits (
        id SERIAL PRIMARY KEY,
        sha TEXT UNIQUE,
        message TEXT,
        author TEXT,
        date TIMESTAMP,
        repo_id INTEGER REFERENCES repos(id)
    );
    """)

    #save the changes
    conn.commit()
    #disconnect cursor
    cur.close()
    #disconnect connection
    conn.close()

