// Connect to the WebSocket server
const socket = new WebSocket('ws://127.0.0.1:8000/chat/ws/chat/');

// Send a message when the "Send" button is clicked
document.getElementById('send-button').addEventListener('click', () => {
  const message = document.getElementById('message-input').value;
  socket.send(message);
});

// Display incoming messages in the chat window
socket.addEventListener('message', (event) => {
  const message = event.data;
  const chatWindow = document.getElementById('chat-window');
  chatWindow.innerHTML += `<p>${message}</p>`;
});
