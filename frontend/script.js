let username
let repo

const API = "https://gitgenie-jkir.onrender.com"

function values(){
 username = document.getElementById("username").value
 repo = document.getElementById("repo").value
}

// Repo Info
async function repoInfo(){

values()

let res = await fetch(`${API}/repo?username=${username}&repo=${repo}`)
let data = await res.json()

document.getElementById("result").innerText =
JSON.stringify(data,null,2)

}

// Contributors
async function contributors(){

values()

let res = await fetch(`${API}/contributors?username=${username}&repo=${repo}`)
let data = await res.json()

document.getElementById("result").innerText =
JSON.stringify(data,null,2)

}

// Commits
async function commits(){

values()

let res = await fetch(`${API}/commits?username=${username}&repo=${repo}`)
let data = await res.json()

document.getElementById("result").innerText =
JSON.stringify(data,null,2)

}

// AI Explain
async function explain(){

values()

let res = await fetch(`${API}/explain?username=${username}&repo=${repo}`)
let data = await res.json()

document.getElementById("result").innerText =
data.explanation

}

// Chat Repo
async function chatRepo(){

values()

let question = prompt("Ask something about repo")

let res = await fetch(`${API}/chat?username=${username}&repo=${repo}&question=${question}`)
let data = await res.json()

document.getElementById("result").innerText =
data.response

}

// Generate README
async function generateReadme(){

values()

let res = await fetch(`${API}/generate-readme?username=${username}&repo=${repo}`)
let data = await res.json()

document.getElementById("result").innerText =
data.readme

}

// Bug Detector
async function detectBugs(){

values()

let res = await fetch(`${API}/bugs?username=${username}&repo=${repo}`)
let data = await res.json()

document.getElementById("result").innerText =
JSON.stringify(data,null,2)

}

// Repo Files
async function showFiles(){

values()

let res = await fetch(`${API}/files?username=${username}&repo=${repo}`)
let data = await res.json()

document.getElementById("result").innerText =
JSON.stringify(data,null,2)

}

// Repo Stats
async function showStats(){

values()

let res = await fetch(`${API}/stats?username=${username}&repo=${repo}`)
let data = await res.json()

document.getElementById("result").innerText =
JSON.stringify(data,null,2)

}

// Explain File
async function explainFile(){

values()

let path = prompt("Enter file path (example: README.md)")

let res = await fetch(`${API}/explain-file?username=${username}&repo=${repo}&path=${path}`)
let data = await res.json()

document.getElementById("result").innerText =
data.explanation

}

// File Tree Explorer
async function loadFileTree(path=""){

values()

let res = await fetch(`${API}/file-tree?username=${username}&repo=${repo}&path=${path}`)
let data = await res.json()

let treeHTML = ""

data.forEach(item => {

if(item.type === "dir"){

treeHTML += `<div class="file folder" onclick="loadFileTree('${item.path}')">📂 ${item.name}</div>`

}else{

treeHTML += `<div class="file" onclick="openFile('${item.path}')">📄 ${item.name}</div>`

}

})

document.getElementById("fileTree").innerHTML = treeHTML

}

// File Preview
async function openFile(path){

values()

let res = await fetch(`${API}/file-content?username=${username}&repo=${repo}&path=${path}`)
let data = await res.json()

document.getElementById("codePreview").textContent = data.content

hljs.highlightAll()

}