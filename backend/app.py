from flask import Flask, redirect, url_for, session, request
from flask_dance.contrib.github import make_github_blueprint, github
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv
import sqlite3
#load an environtment with variables set in an .env file
load_dotenv()

#this allows us to use HTTP, as OAuth2 requires HTTPS for security
#if ever gets past interanal use, REMOVE THIS
#TODO: REMOVE THIS IF PAST INTERNAL USE AND TESTING
os.environ["OATHLIB_INSECURE_TRANSPORT"] = os.getenv("OAUTHLIB_INSECURE_TRANSPORT", "1")

#initalize Flask web application, and enable Cross-Origin Resource Sharing
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersekrit")
CORS(app)

#creates a login blueprint with the GitHub credentials
#then mounts it at the "/login" path, ex. "/login/github"
#the scope is added to allow for acces to both public and private repos
blueprint = make_github_blueprint(
    client_id = os.getenv("GITHUB_OAUTH_CLIENT_ID"),
    client_secret = os.getenv("GITHUB_OAUTH_CLIENT_SECRET"),
    scope = "repo"
)
app.register_blueprint(blueprint, url_prefix = "/login")

#tells Flask to execute index when the root URL is accessed either by 
#browser or HTTP GET request
@app.route("/")
def index():
    if not github.authorized:
        return redirect(url_for("github.login"))
    #response with user info
    resp = github.get("/user")
    if not resp.ok:
        return f"Github API Error: {resp.text}", 500
    #done to prevent error, to note, if it displays unknow, then it fails
    data = resp.json()
    username = data.get("login", "Unknown")
    return f"You are logged in as: {username}"

#this function will execute when we go to the /repos URL
@app.route("/repos")
def get_repos():
    #PAT used
    pat_token = request.headers.get("Authorization")
    if pat_token:
        HEADERS = {
            "Accept": "application/vnd.github+json",
            "Authorization": pat_token,
            "X-GitHub-Api-Version": "2022-11-28"
        }

        #now call the GIT API with the PAT
        resp = requests.get("https://api.github.com/user/repos", headers=HEADERS)
        if not resp.ok:
            return f"Failed to fetch repos<PAT USAGE>: {resp.text}", 500
        
        repo_data = resp.json()
        simplified = [{"name": r["name"], "full_name": r["full_name"]} for r in repo_data]
        return {"repos": simplified}
    #no PAT used
    if not github.authorized:
        return redirect(url_for("github.login"))
    
    #response with all the repos
    resp = github.get("/user/repos")

    #failure case, with 500 HTTP status code(Interal Server Error)
    if not resp.ok:
        return f"Failed to fetch repos: {resp.text}", 500
    
    repo_data = resp.json()
    #will return name + full_name for now
    simplified = [{"name": r["name"], "full_name": r["full_name"]} for r in repo_data]
    return {"repos": simplified}

#this function will execute when we go to /commits
@app.route("/commits")
def get_commits():
    #to be changed for ease of use, currently must manually choose the repos
    repo_full_name = request.args.get("repo")
    if not repo_full_name:
        return {"error": "Missing 'repo' query parameter"}, 400
    
    #personal access token, this is done to allow etl automatic scraping
    pat_token = request.headers.get("Authorization")
    if pat_token:
        header = {
            "Accept": "application/vnd.github+json",
            "Authorization": pat_token,
            "X-GitHub-Api-Version": "2022-11-28"
        }
        #we now get the commit history, currently set to only return the last 10 commits to limit stress
        url = f"https://api.github.com/repos/{repo_full_name}/commits"
        resp = requests.get(url, headers=header)
        if not resp.ok:
            return f"Failed to fetch commits: {resp.text}", 500
        
        #this is where we manipulate the data, currently jsut getting metadata
        commit_data = resp.json()
        simplified = []
        for c in commit_data:
            simplified.append({
                "sha": c["sha"],
                "message": c["commit"]["message"],
                "author": c["commit"]["author"]["name"],
                "date": c["commit"]["author"]["date"]
            })
        return {"commits": simplified}
    
    #no token so we are manually accessing it
    if not github.authorized:
        return redirect(url_for("github.login"))
    
    resp = github.get(f"/repos/{repo_full_name}/commits?per_page=10")
    if not resp:
        return f"Failed to get the commit history: {resp.text}", 500
    
    commit_data = resp.json()
    simplified = []
    for c in commit_data:
        simplified.append({
            "sha": c["sha"],
            "message": c["commit"]["message"],
            "author": c["commit"]["author"]["name"],
            "date": c["commit"]["author"]["date"]
        })
    return {"commits": simplified}

###----------STATS----------###
@app.route("/api/stats/commits-per-day")
def commits_per_day():
    author = request.args.get("author")
    repo = request.args.get("repo")
    
    conn = sqlite3.connect("devinsight.db")
    cur = conn.cursor()

    query = """
            SELECT c.date
            FROM commits c
            JOIN repos r ON c.repo_id = r.id
            WHERE 1=1
    """
    params = []
    
    if author:
        query += " AND c.author = ?"
        params.append(author)
    
    if repo:
        query += " AND r.full_name = ?"
        params.append(repo)
    
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()

    from collections import defaultdict
    from datetime import datetime

    daily_counts = defaultdict(int)
    for (date_str,) in rows:
        try:
            date = datetime.fromisoformat(date_str).date()
        except ValueError:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        daily_counts[str(date)] += 1
    
    sorted_counts = sorted(daily_counts.items())
    return jsonify([{"date": d, "count": c} for d, c in sorted_counts])
###-----------------------------------###
###             DEBUG                 ###

#this function is used to determine the rate limit
#and the remaining amount of tokens
@app.route("/rate_limit")
def check_rate_limit():
    if not github.authorized:
        return redirect(url_for("github.login"))

    resp = github.get("/rate_limit")
    return resp.json()


if __name__ == "__main__":
    app.run(debug = True)
