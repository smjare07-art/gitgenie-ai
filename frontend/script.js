let username
let repo

function values(){
 username = document.getElementById("username").value
 repo = document.getElementById("repo").value
}

const API = "https://gitgenie-jkir.onrender.com"

async function repoInfo(){

values()

let res = await fetch(`${API}/repo?username=${username}&repo=${repo}`)
let data = await res.json()

document.getElementById("result").innerText =
JSON.stringify(data,null,2)

}

async function contributors(){

values()

let res = await fetch(`${API}/contributors?username=${username}&repo=${repo}`)
let data = await res.json()

document.getElementById("result").innerText =
JSON.stringify(data,null,2)

}

async function commits(){

values()

let res = await fetch(`${API}/commits?username=${username}&repo=${repo}`)
let data = await res.json()

document.getElementById("result").innerText =
JSON.stringify(data,null,2)

}

async function explain(){

values()

let res = await fetch(`${API}/explain?username=${username}&repo=${repo}`)
let data = await res.json()

document.getElementById("result").innerText =
data.explanation

}

async function chatRepo(){

values()

let question = prompt("Ask something about repo")

let res = await fetch(`${API}/chat?username=${username}&repo=${repo}&question=${question}`)
let data = await res.json()

document.getElementById("result").innerText =
data.response

}

async function generateReadme(){

values()

let res = await fetch(`${API}/generate-readme?username=${username}&repo=${repo}`)
let data = await res.json()

document.getElementById("result").innerText =
data.readme

}

async function detectBugs(){

values()

let res = await fetch(`${API}/bugs?username=${username}&repo=${repo}`)
let data = await res.json()

document.getElementById("result").innerText =
JSON.stringify(data,null,2)

}

async function showFiles(){

values()

let res = await fetch(`${API}/files?username=${username}&repo=${repo}`)
let data = await res.json()

document.getElementById("result").innerText =
JSON.stringify(data,null,2)

}

async function showStats(){

values()

let res = await fetch(`${API}/stats?username=${username}&repo=${repo}`)
let data = await res.json()

document.getElementById("result").innerText =
JSON.stringify(data,null,2)

}

async function explainFile(){

values()

let path = prompt("Enter file path (example: README.md)")

let res = await fetch(`${API}/explain-file?username=${username}&repo=${repo}&path=${path}`)
let data = await res.json()

document.getElementById("result").innerText =
data.explanation

}

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

async function openFile(path){

values()

let res = await fetch(`${API}/file-content?username=${username}&repo=${repo}&path=${path}`)
let data = await res.json()

document.getElementById("codePreview").textContent = data.content

hljs.highlightAll()

}