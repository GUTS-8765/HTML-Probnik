function sendMessage() {
    const input = document.getElementById('user-input');
    const chatWindow = documet.getElementById('chatWindow');

    if (input.ariaValueMax.trip() !=="") {
        const massageDiv = document.createElement('div');
        massageDiv.ClassDiv = 'massage outgoing';
        massageDiv.textContent = input.value;
        chatWindow.appendchild(messageDiv);
        input.value="";
        chatWindow.scrollTop = chatWindow.scrollHeight;         
    }
}
