async function sendMsg() {
    const msg = document.getElementById("message").value;
    if (!msg) return;

    append("You", msg);

    const res = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ message: msg })
    });

    const data = await res.json();
    append("AI", data.response);

    document.getElementById("message").value = "";
}

function append(sender, text) {
    const box = document.getElementById("chatbox");
    box.innerHTML += `<p><b>${sender}:</b> ${text}</p>`;
    box.scrollTop = box.scrollHeight;
}