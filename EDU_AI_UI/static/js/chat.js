document.addEventListener("DOMContentLoaded", function() {
    const sendBtn = document.querySelector('.send-btn');
    const chatInput = document.getElementById('chat-input');
    const chatContent = document.getElementById('chat-content');
    const chatHistory = document.getElementById('chat-history');
    const welcomeText = document.getElementById('welcome-text');
    let isFirstMessage = true;

    function createTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'typing-indicator';
        typingDiv.innerHTML = `
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        `;
        return typingDiv;
    }

    function handleFirstMessage() {
        if (isFirstMessage) {
            welcomeText.classList.add('hidden');
            chatContent.classList.remove('hidden');
            // Remove the 'initial' class so the input shifts to the bottom
            document.querySelector('.chat-container').classList.remove('initial');
            isFirstMessage = false;
            
            setTimeout(() => {
                chatContent.style.marginTop = '20px';
            }, 300);
        }
    }

    function sendMessage() {
        let message = chatInput.value.trim();
        if (message !== "") {
            handleFirstMessage();
            appendMessage("user", message);
            chatInput.value = "";
            
            // Show loading state
            sendBtn.classList.add('loading');
            
            // Show typing indicator
            const typingIndicator = createTypingIndicator();
            chatHistory.appendChild(typingIndicator);
            
            // Scroll to the typing indicator
            typingIndicator.scrollIntoView({ behavior: "smooth", block: "end" });

            // Send message to AI
            sendMessageToAI(message, typingIndicator);
        }
    }

    function sendMessageToAI(message, typingIndicator) {
        // Simulate network delay (remove this in production)
        setTimeout(() => {
            fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: message })
            })
            .then(response => response.json())
            .then(data => {
                // Remove typing indicator
                typingIndicator.remove();
                
                // Remove loading state
                sendBtn.classList.remove('loading');
                
                let aiResponse = data.reply || "No response from AI.";
                appendMessage("ai", aiResponse);
            })
            .catch(error => {
                console.error('Error:', error);
                typingIndicator.remove();
                sendBtn.classList.remove('loading');
                appendMessage("ai", "Sorry, there was an error processing your message.");
            });
        }, 500); // Simulate network delay
    }

    function appendMessage(sender, message) {
        const messageElem = document.createElement("div");
        messageElem.classList.add("message", sender);
        messageElem.textContent = message;
        chatHistory.appendChild(messageElem);
        
        // Scroll to the new message
        messageElem.scrollIntoView({ behavior: "smooth", block: "end" });
    }

    sendBtn.addEventListener('click', sendMessage);

    chatInput.addEventListener('keydown', function(e) {
        if (e.key === "Enter") {
            e.preventDefault();
            sendMessage();
        }
    });
});
