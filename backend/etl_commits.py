import requests
import sqlite3
import os
from dotenv import load_dotenv
load_dotenv()
#configuration
#TODO: AUTOMATE FOR ALL REPOS, currently testing only one
REPO = "OGCbn/devinsight"
BACKEND_URL = f"http://localhost:5000/commits?repo={REPO}"
GITHUB_PAT = os.getenv("GITHUB_PAT")
DB_PATH = os.path.join(os.path.dirname(__file__), "devinsight.db")

#fetch commits
def fetch_commits():
    print(f"Fetching commits for {REPO}")
    headers = {
        "Authorization": GITHUB_PAT
    }
    resp = requests.get(BACKEND_URL, headers=headers)
    if resp.status_code != 200:
        print("Failed to fetch commits", resp.text)
        return []
    return resp.json()["commits"]
    
#Insert the commits into the database
def insert_commits(commits, repo_name):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    #placeholder repo entry
    cur.execute("INSERT OR IGNORE INTO repos (full_name, user_id) VALUES (?, ?)", (repo_name, 1))
    conn.commit()

    #get the repo_id
    cur.execute("SELECT id FROM repos WHERE full_name = ?", (repo_name,))
    repo_id = cur.fetchone()[0]

    for c in commits:
        cur.execute("""
            INSERT OR IGNORE INTO commits (sha, message, author, date, repo_id)
            VALUES (?, ?, ?, ?, ?)
        """, (c["sha"], c["message"], c["author"], c["date"], repo_id))

    conn.commit()
    cur.close()
    conn.close()
    print(f"Inserted {len(commits)} commits into the database.")

if __name__ == "__main__":
    commits = fetch_commits()
    if commits:
        insert_commits(commits)
    else:
        print("Error, no commits returned")