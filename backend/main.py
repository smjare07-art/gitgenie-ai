# GitGenie AI
# Developed by Shubham Jare

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import base64

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Home
@app.get("/")
def home():
    return {"message": "GitGenie AI Running"}

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}

# Repo Info
@app.get("/repo")
def repo_info(username: str, repo: str):

    url = f"https://api.github.com/repos/{username}/{repo}"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "Repository not found"}

    data = response.json()

    return {
        "name": data.get("name"),
        "description": data.get("description"),
        "stars": data.get("stargazers_count"),
        "language": data.get("language")
    }

# Contributors
@app.get("/contributors")
def repo_contributors(username: str, repo: str):

    url = f"https://api.github.com/repos/{username}/{repo}/contributors"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "Cannot fetch contributors"}

    data = response.json()

    result = []

    for c in data[:5]:
        result.append({
            "name": c.get("login"),
            "contributions": c.get("contributions")
        })

    return result

# Commits
@app.get("/commits")
def repo_commits(username: str, repo: str):

    url = f"https://api.github.com/repos/{username}/{repo}/commits"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "Cannot fetch commits"}

    data = response.json()

    commits = []

    for c in data[:5]:

        commit = c.get("commit", {})
        author = commit.get("author", {})

        commits.append({
            "author": author.get("name", "Unknown"),
            "message": commit.get("message", "No message")
        })

    return commits

# Repo Explanation
@app.get("/explain")
def explain_repo(username: str, repo: str):

    url = f"https://api.github.com/repos/{username}/{repo}"
    data = requests.get(url).json()

    explanation = f"""
Project Name: {data.get('name')}

Description:
{data.get('description')}

Language Used:
{data.get('language')}

Stars:
{data.get('stargazers_count')}

This project is mainly built using {data.get('language')} and is popular with {data.get('stargazers_count')} stars on GitHub.
"""

    return {"explanation": explanation}

# Chat Repo
@app.get("/chat")
def chat_with_repo(username: str, repo: str, question: str):

    url = f"https://api.github.com/repos/{username}/{repo}"
    data = requests.get(url).json()

    answer = f"""
Repository: {data.get('name')}

Question: {question}

Answer:
This project is mainly built using {data.get('language')}.
It has {data.get('stargazers_count')} stars on GitHub.

Description:
{data.get('description')}
"""

    return {"response": answer}

# README Generator
@app.get("/generate-readme")
def generate_readme(username: str, repo: str):

    url = f"https://api.github.com/repos/{username}/{repo}"
    data = requests.get(url).json()

    readme = f"""
# {data.get('name')}

## Description
{data.get('description')}

## Tech Stack
{data.get('language')}

## Stars
⭐ {data.get('stargazers_count')}

## Installation

git clone https://github.com/{username}/{repo}.git
cd {repo}

## Author
GitHub: https://github.com/{username}
"""

    return {"readme": readme}

# Bug Detector
@app.get("/bugs")
def bug_detector(username: str, repo: str):

    url = f"https://api.github.com/repos/{username}/{repo}/issues"
    data = requests.get(url).json()

    bugs = []

    for issue in data[:5]:

        title = issue.get("title", "")

        if "bug" in title.lower():
            bugs.append(title)

    return {"possible_bugs": bugs}

# Repo Files
@app.get("/files")
def repo_files(username: str, repo: str):

    url = f"https://api.github.com/repos/{username}/{repo}/contents"
    data = requests.get(url).json()

    files = []

    if isinstance(data, list):

        for item in data:
            files.append({
                "name": item.get("name"),
                "type": item.get("type")
            })

    return files

# Repo Stats
@app.get("/stats")
def repo_stats(username: str, repo: str):

    url = f"https://api.github.com/repos/{username}/{repo}"
    data = requests.get(url).json()

    return {
        "stars": data.get("stargazers_count"),
        "forks": data.get("forks_count"),
        "watchers": data.get("watchers_count")
    }

# Explain File / Folder
@app.get("/explain-file")
def explain_file(username: str, repo: str, path: str):

    url = f"https://api.github.com/repos/{username}/{repo}/contents/{path}"
    data = requests.get(url).json()

    if isinstance(data, list):

        files = [item.get("name") for item in data]

        explanation = f"""
Folder: {path}

Files inside:
{', '.join(files)}
"""

    else:

        explanation = f"""
File: {data.get('name')}

This file belongs to repository {repo}.
"""

    return {"explanation": explanation}

# File Tree
@app.get("/file-tree")
def file_tree(username: str, repo: str, path: str = ""):

    url = f"https://api.github.com/repos/{username}/{repo}/contents/{path}"
    data = requests.get(url).json()

    tree = []

    if isinstance(data, list):

        for item in data:
            tree.append({
                "name": item.get("name"),
                "type": item.get("type"),
                "path": item.get("path")
            })

    return tree

# File Content Preview
@app.get("/file-content")
def file_content(username: str, repo: str, path: str):

    url = f"https://api.github.com/repos/{username}/{repo}/contents/{path}"
    data = requests.get(url).json()

    if "content" in data:

        content = base64.b64decode(data["content"]).decode("utf-8", errors="ignore")

    else:
        content = "Cannot preview this file"

    return {"content": content}