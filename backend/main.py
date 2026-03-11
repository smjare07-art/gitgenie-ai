from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def home():
    return{"message":"GitGenie AI Running"}
@app.get("/repo")
def repo_info(username:str,repo:str):
    url=f"https://api.github.com/repos/{username}/{repo}"
    data=requests.get(url).json()

    return{
        "name":data["name"],
        "description":data["description"],
        "stars":data["stargazers_count"],
        "language":data["language"],
    }
@app.get("/contributors")
def repo_contributors(username: str, repo: str):

    url = f"https://api.github.com/repos/{username}/{repo}/contributors"
    data = requests.get(url).json()

    result = []

    for c in data[:5]:
        result.append({
            "name": c["login"],
            "contributions": c["contributions"]
        })

    return result
@app.get("/commits")
def repo_commits(username: str, repo: str):

    url = f"https://api.github.com/repos/{username}/{repo}/commits"
    data = requests.get(url).json()

    commits = []

    for c in data[:5]:
        commits.append({
            "author": c["commit"]["author"]["name"],
            "message": c["commit"]["message"]
        })

    return commits
@app.get("/explain")
def explain_repo(username: str, repo: str):

    url = f"https://api.github.com/repos/{username}/{repo}"
    data = requests.get(url).json()

    explanation = f"""
    Project Name: {data['name']}

    Description:
    {data['description']}

    Language Used:
    {data['language']}

    Stars:
    {data['stargazers_count']}

    This project is mainly built using {data['language']} 
    and is popular with {data['stargazers_count']} stars on GitHub.
    """

    return {"explanation": explanation}
@app.get("/chat")
def chat_with_repo(username: str, repo: str, question: str):

    url = f"https://api.github.com/repos/{username}/{repo}"
    data = requests.get(url).json()

    answer = f"""
    Repository: {data['name']}

    Question: {question}

    Answer:
    This project is mainly built using {data['language']}.
    It has {data['stargazers_count']} stars on GitHub.

    Description:
    {data['description']}
    """

    return {"response": answer}
@app.get("/generate-readme")
def generate_readme(username: str, repo: str):

    url = f"https://api.github.com/repos/{username}/{repo}"
    data = requests.get(url).json()

    readme = f"""
# {data['name']}

## Description
{data['description']}

## Tech Stack
{data['language']}

## Stars
⭐ {data['stargazers_count']}

## Installation

git clone https://github.com/{username}/{repo}.git
cd {repo}

## Author
GitHub: https://github.com/{username}
"""

    return {"readme": readme}
@app.get("/bugs")
def bug_detector(username: str, repo: str):

    url = f"https://api.github.com/repos/{username}/{repo}/issues"
    data = requests.get(url).json()

    bugs = []

    for issue in data[:5]:
        if "bug" in issue["title"].lower():
            bugs.append(issue["title"])

    return {"possible_bugs": bugs}
@app.get("/files")
def repo_files(username: str, repo: str):

    url = f"https://api.github.com/repos/{username}/{repo}/contents"
    data = requests.get(url).json()

    files = []

    for item in data:
        files.append({
            "name": item["name"],
            "type": item["type"]
        })

    return files
@app.get("/stats")
def repo_stats(username: str, repo: str):

    url = f"https://api.github.com/repos/{username}/{repo}"
    data = requests.get(url).json()

    return {
        "stars": data["stargazers_count"],
        "forks": data["forks_count"],
        "watchers": data["watchers_count"]
    }
@app.get("/explain-file")
def explain_file(username: str, repo: str, path: str):

    url = f"https://api.github.com/repos/{username}/{repo}/contents/{path}"
    data = requests.get(url).json()

    # If folder
    if isinstance(data, list):

        files = [item["name"] for item in data]

        explanation = f"""
Folder: {path}

This is a directory in the repository.

Files inside:
{', '.join(files)}

This folder likely contains project related resources.
"""

    else:

        explanation = f"""
File: {data['name']}

This file belongs to repository {repo}.

It is likely used for implementing project functionality.
"""

    return {"explanation": explanation}
@app.get("/file-tree")
def file_tree(username: str, repo: str, path: str = ""):

    url = f"https://api.github.com/repos/{username}/{repo}/contents/{path}"
    data = requests.get(url).json()

    tree = []

    for item in data:
        tree.append({
            "name": item["name"],
            "type": item["type"],
            "path": item["path"]
        })

    return tree
import base64

@app.get("/file-content")
def file_content(username: str, repo: str, path: str):

    url = f"https://api.github.com/repos/{username}/{repo}/contents/{path}"
    data = requests.get(url).json()

    if "content" in data:
        content = base64.b64decode(data["content"]).decode("utf-8", errors="ignore")
    else:
        content = "Cannot preview this file"

    return {"content": content}