const chatArea = document.getElementById("chat-area");
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");

function addMessage(role, text) {
  const message = document.createElement("div");
  message.classList.add("message");
  message.classList.add(role === "user" ? "user-message" : "bot-message");

  const label = document.createElement("span");
  label.className = "message-role";
  label.textContent = role === "user" ? "You" : "AI";

  const content = document.createElement("p");
  content.textContent = text;

  message.appendChild(label);
  message.appendChild(content);
  chatArea.appendChild(message);
  chatArea.scrollTop = chatArea.scrollHeight;
}

async function sendMessage(text) {
  const response = await fetch("/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text }),
  });

  if (!response.ok) {
    addMessage("bot", "There was a problem processing your request. Please try again.");
    return;
  }

  const data = await response.json();
  if (data.error) {
    addMessage("bot", data.error);
    return;
  }

  const botText = `Predicted disease: ${data.disease}. Confidence: ${data.confidence}%. Advice: ${data.advice}`;
  addMessage("bot", botText);
}

chatForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const message = chatInput.value.trim();
  if (!message) {
    return;
  }

  addMessage("user", message);
  chatInput.value = "";
  sendMessage(message);
});
