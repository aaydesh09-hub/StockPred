async function sendMsg() {
    const input = document.getElementById("message");
    const msg = input.value.trim();
    if (!msg) return;

    append("You", msg);

    const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: msg })
    });

    const data = await res.json();
    append("AI", data.response);

    input.value = "";
}

function escapeHTML(text) {
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
}

function append(sender, text) {
    const box = document.getElementById("chatbox");

    const roleClass = sender === "You" ? "chat-user" : "chat-bot";

    box.innerHTML += `
        <div class="chat-message ${roleClass}">
            <strong>${sender}</strong>
${escapeHTML(text)}
        </div>
    `;

    box.scrollTop = box.scrollHeight;
}


