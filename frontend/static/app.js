console.log("APP JS LOADED");

document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM CONTENT LOADED");

    const sendBtn = document.getElementById("sendBtn");
    console.log(sendBtn);

    const sendBtn = document.getElementById("sendBtn");
    const userInput = document.getElementById("userInput");
    const chatMessages = document.getElementById("chatMessages");

    async function sendMessage() {

        const message = userInput.value.trim();

        if (!message) return;

        const userDiv = document.createElement("div");
        userDiv.className = "message user";
        userDiv.innerText = message;

        chatMessages.appendChild(userDiv);

        userInput.value = "";

        try {

            const response = await fetch("/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    message: message
                })
            });

            const data = await response.json();

            const botDiv = document.createElement("div");
            botDiv.className = "message bot";
            botDiv.innerText = data.response;

            chatMessages.appendChild(botDiv);

            chatMessages.scrollTop =
                chatMessages.scrollHeight;

        } catch (error) {

            console.error(error);

            const botDiv = document.createElement("div");
            botDiv.className = "message bot";
            botDiv.innerText = "Server Error";

            chatMessages.appendChild(botDiv);
        }
    }

    sendBtn.addEventListener("click", sendMessage);

    userInput.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            sendMessage();
        }
    });

});