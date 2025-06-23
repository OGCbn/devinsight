import requests
import sqlite3
import os
from dotenv import load_dotenv
from etl_commits import insert_commits #reuse insert logic

load_dotenv()

#Config
BACKEND_REPOS_URL = "http://localhost:5000/repos"
BACKEND_COMMITS_URL = "http://localhost:5000/commits?repo="
GITHUB_PAT = os.getenv("GITHUB_PAT")
DB_PATH = os.path.join(os.path.dirname(__file__), "devinsight.db")

HEADERS = {
    "Authorization": GITHUB_PAT,
    "X-GitHub-Api-Version": "2022-11-28"
}

def fetch_all_repos():
    print("Fetching list of all repos")
    resp = requests.get(BACKEND_REPOS_URL, headers=HEADERS)

    if resp.status_code != 200:
        print("Failed to fetch repos:", resp.text)
        return []
    print(resp)
    return resp.json().get("repos", [])

#this will be called in the main function for every repo return 
#from the fetch_all_repos function
def fetch_commits_for_repo(full_name):
    print(f"\nFetching commits for: {full_name}")
    resp = requests.get(f"{BACKEND_COMMITS_URL}{full_name}", headers=HEADERS)
    if resp.status_code != 200:
        print(f"Failure in fetching commits for {full_name}: {resp.text}")
        return []
    #list of full commits history
    return resp.json().get("commits", [])

if __name__ == "__main__":
    repos = fetch_all_repos()
    if not repos:
        print("No repos found.")
        exit(1)
    
    #at least one repo is found
    for repo in repos:
        full_name = repo["full_name"]
        commits = fetch_commits_for_repo(full_name)
        #has commits,<always TRUE unless error in fetching>
        if commits:
            insert_commits(commits, full_name)
        else:
            print("No commits found for {full_name}")
