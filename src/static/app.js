const chat = document.getElementById("chat");
const form = document.getElementById("composer");
const input = document.getElementById("question");
const template = document.getElementById("msg-template");
const sendButton = document.getElementById("send");

function addMessage(role, text, sources = []) {
  const node = template.content.firstElementChild.cloneNode(true);
  node.classList.add(role);
  node.querySelector(".role").textContent = role === "assistant" ? "Alyssa" : "You";

  const bubble = node.querySelector(".bubble");
  bubble.textContent = text;

  if (role === "assistant" && sources.length) {
    const sourceWrap = document.createElement("div");
    sourceWrap.className = "sources";
    for (const src of sources) {
      const pill = document.createElement("span");
      pill.className = "source-pill";
      pill.textContent = src;
      sourceWrap.appendChild(pill);
    }
    bubble.appendChild(sourceWrap);
  }

  chat.appendChild(node);
  chat.scrollTop = chat.scrollHeight;
}

async function ask(question) {
  addMessage("user", question);
  sendButton.disabled = true;
  addMessage("assistant", "Thinking...");
  const thinkingNode = chat.lastElementChild;

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });

    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.error || "Request failed");
    }

    thinkingNode.remove();
    addMessage("assistant", payload.answer, payload.retrieved_sections || []);
  } catch (err) {
    thinkingNode.remove();
    addMessage("assistant", `I hit an error: ${err.message}`);
  } finally {
    sendButton.disabled = false;
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const q = input.value.trim();
  if (!q) return;
  input.value = "";
  await ask(q);
});

document.querySelectorAll(".chip").forEach((chip) => {
  chip.addEventListener("click", () => {
    const q = chip.getAttribute("data-q");
    input.value = q;
    input.focus();
  });
});

addMessage(
  "assistant",
  "Hi, I am Alyssa. Ask me about Jessup CS admissions, classes, tuition, exams, or campus services."
);
