const form = document.getElementById('chat-form');
const input = document.getElementById('message');
const chat = document.getElementById('chat');


function appendMessage(text, cls) {
  const d = document.createElement('div');
  d.className = 'msg ' + cls;
  const avatar = document.createElement('div');
  avatar.className = 'avatar';
  avatar.textContent = cls === 'user' ? '🧑' : '🤖';
  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.textContent = text;
  if (cls === 'user') {
    d.appendChild(bubble);
    d.appendChild(avatar);
  } else {
    d.appendChild(avatar);
    d.appendChild(bubble);
  }
  chat.appendChild(d);
  chat.scrollTop = chat.scrollHeight;
}

function setTyping(show) {
  document.getElementById('typing-indicator').style.display = show ? '' : 'none';
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const msg = input.value.trim();
  if (!msg) return;
  appendMessage(msg, 'user');
  input.value = '';
  setTyping(true);
  try {
    const resp = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: msg }),
    });
    const data = await resp.json();
    setTyping(false);
    if (data.error) {
      appendMessage('Error: ' + data.error, 'assistant');
    } else {
      appendMessage(data.reply ?? '', 'assistant');
    }
  } catch (err) {
    setTyping(false);
    appendMessage('Network error', 'assistant');
  }
});

// Auto-focus input on load and after sending
window.onload = () => {
  input.focus();
};
input.addEventListener('blur', () => setTimeout(() => input.focus(), 100));
