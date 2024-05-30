document.addEventListener('DOMContentLoaded', function() {
    const username = document.getElementById('username-input').value;

    const chatSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/chat/$'
    );

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const chatLog = document.querySelector('#chat-log');
        const newMessage = document.createElement('div');
        newMessage.textContent = `${data.username}: ${data.message}`;
        chatLog.appendChild(newMessage);
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    document.querySelector('#chat-message-submit').onclick = function(e) {
        const messageInputDom = document.querySelector('#chat-message-input');
        const message = messageInputDom.value;
        if (message.trim() !== '') {
            chatSocket.send(JSON.stringify({
                'message': message,
                'username': username
            }));
            messageInputDom.value = '';
        }
    };

    document.querySelector('#chat-message-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            document.querySelector('#chat-message-submit').click();
        }
    });
});
