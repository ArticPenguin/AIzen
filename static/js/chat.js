const chatBox = document.getElementById("chat-box");
const input = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

const CHAT_API = window.location.origin + "/chat";

sendBtn.onclick = send;
input.onkeydown = e => e.key === "Enter" && send();

async function send() {
    const text = input.value.trim();
    if (!text) return;

    add("user", text);
    input.value = "";

    const aiDiv = add("ai", "");

    const res = await fetch(CHAT_API, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text })
    });

    const reader = res.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        aiDiv.textContent += decoder.decode(value);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
}

function add(role, text) {
    const div = document.createElement("div");
    div.className = `msg ${role}`;
    div.textContent = text;
    chatBox.appendChild(div);
    return div;
}
