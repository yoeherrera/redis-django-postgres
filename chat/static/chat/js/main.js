// main.js

document.addEventListener('DOMContentLoaded', function() {
    var chatSocket = new WebSocket('ws://' + window.location.host + '/ws/chat/');

    chatSocket.onmessage = function(e) {
        var data = JSON.parse(e.data);
        var message = data['message'];
        var username = data['username'];

        // Display the message in the chat log
        var chatLog = document.getElementById('chat-log');
        chatLog.innerHTML += '<p><strong>' + username + '</strong>: ' + message + '</p>';
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    // Function to send a message via WebSocket
    document.querySelector('#chat-message-submit').onclick = function(e) {
        var messageInputDom = document.querySelector('#chat-message-input');
        var message = messageInputDom.value;
        chatSocket.send(JSON.stringify({
            'message': message
        }));
        messageInputDom.value = '';
    };

    // Optional: Function to handle pressing Enter to send a message
    document.querySelector('#chat-message-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            document.querySelector('#chat-message-submit').click();
        }
    });
});
