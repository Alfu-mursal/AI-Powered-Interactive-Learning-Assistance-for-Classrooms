
let prompt = document.querySelector("#prompt");
let container = document.querySelector(".container");
let btn = document.querySelector("#btn");
let chatContainer = document.querySelector(".chat-container");
let userMessage = null;
let API_URL = 'http://localhost:5000/chat';

function createChatBox(html, className) {
    let div = document.createElement("div");
    div.classList.add(className);
    div.innerHTML = html;
    return div;
}

async function getApiResponse(aiChatBox) {
    let textElement = aiChatBox.querySelector(".text");
    try {
        let response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userMessage })
        });
        let data = await response.json();
        textElement.innerText = data.response;
    } catch (error) {
        textElement.innerText = "Error fetching response.";
    } finally {
        aiChatBox.querySelector(".loading").style.display = "none";
    }
}

function showLoading() {
    let html = `<div class="img"><img src="ai.png" alt="" width="50"></div>
                 <p class="text"></p>
                 <img class="loading" src="loading.gif" alt="loading" height="50">`;
    let aiChatBox = createChatBox(html, "ai-chat-box");
    chatContainer.appendChild(aiChatBox);
    getApiResponse(aiChatBox);
}

btn.addEventListener("click", () => {
    userMessage = prompt.value;
    if (!userMessage) {
        container.style.display = "flex";
        return;
    }
    container.style.display = "none";
    let html = `<div class="img"><img src="user.png" alt="" width="50"></div>
                 <p class="text"></p>`;
    let userChatBox = createChatBox(html, "user-chat-box");
    userChatBox.querySelector(".text").innerText = userMessage;
    chatContainer.appendChild(userChatBox);
    prompt.value = "";
    setTimeout(showLoading, 500);
});
