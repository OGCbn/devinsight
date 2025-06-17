from flask import Flask, redirect, url_for, session
from flask_dance.contrib.github import make_github_blueprint, github
from flask_cors import CORS
import os
from dotenv import load_dotenv

#load an environtment with variables set in an .env file
load_dotenv()

#initalize Flask web application, and enable Cross-Origin Resource Sharing
app = Flask(_name_)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersekrit")
CORS(app)

#creates a login blueprint with the GitHub credentials
#then mounts it at the "/login" path, ex. "/login/github"
blueprint = make_github_blueprint(
    client_id = os.getenv("GITHUB_OAUTH_CLIENT_ID"),
    client_secret = os.getenv("GITHUB_OAUTH_CLIENT_SECRET"),
)
app.register_blueprint(blueprint, url_prefix = "/login")

#tells Flask to execute index when the root URL is accessed either by 
#browser or HTTP GET request
@app.route("/")
def index():
    if not github.authorized:
        return redirect(url_for("github.login"))
    resp = github.get("/user")
    return f"You are logged in as: {resp.json()['login']}"

if __name__ == "__main__":
    app.run(debug = True)
