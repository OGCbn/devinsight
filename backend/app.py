from flask import Flask, redirect, url_for, session, request
from flask_dance.contrib.github import make_github_blueprint, github
from flask_cors import CORS
import os
from dotenv import load_dotenv

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
    #failure case
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
    #failure case
    if not github.authorized:
        return redirect(url_for("github.login"))
    
    #to be changed for ease of use, currently must manually choose the repos
    repo_full_name = request.args.get("repo")
    if not repo_full_name:
        return {"error": "Missing 'repo' query parameter"}, 400
    
    #we now get the commit history, currently set to only return the last 10 commits to limit stress
    resp = github.get(f"/repos/{repo_full_name}/commits?per_page=10")
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
