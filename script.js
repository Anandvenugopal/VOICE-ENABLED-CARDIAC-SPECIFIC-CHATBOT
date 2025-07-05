document.addEventListener('DOMContentLoaded', () => {
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-btn');
    const chatMessages = document.getElementById('chat-messages');
    const fileInput = document.getElementById('file-input');
    const filePreview = document.getElementById('file-preview');
    const voiceButton = document.getElementById('voice-btn');
    const voiceIndicator = document.getElementById('voice-indicator');
    const themeToggle = document.getElementById('theme-toggle');

    let isRecording = false;
    let mediaRecorder = null;
    let audioChunks = [];
    let currentBotMessage = null;
    let currentMessageContent = '';
    
    // Configure marked.js
    marked.setOptions({
        breaks: true,
        gfm: true,
        headerIds: false,
        mangle: false
    });
    
    // Theme Toggle
    themeToggle.addEventListener('click', () => {
        document.body.setAttribute('data-theme', 
            document.body.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'
        );
        themeToggle.innerHTML = document.body.getAttribute('data-theme') === 'dark' 
            ? '<i class="fas fa-sun"></i>' 
            : '<i class="fas fa-moon"></i>';
    });

    // Auto-resize textarea
    messageInput.addEventListener('input', () => {
        messageInput.style.height = 'auto';
        messageInput.style.height = messageInput.scrollHeight + 'px';
    });

    // Send message on Enter (Shift+Enter for new line)
    messageInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Send message function
    async function sendMessage() {
        const message = messageInput.value.trim();
        if (message || filePreview.children.length > 0) {
            addMessage(message, 'user');
            messageInput.value = '';
            messageInput.style.height = 'auto';
            
            try {
                // Create a placeholder for the bot's response
                currentBotMessage = createBotMessageElement('');
                currentMessageContent = '';
                chatMessages.appendChild(currentBotMessage);
                chatMessages.scrollTop = chatMessages.scrollHeight;

                const response = await fetch('http://localhost:5000/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'text/event-stream',
                    },
                    body: JSON.stringify({ message: message })
                });

                const reader = response.body.getReader();
                const decoder = new TextDecoder();

                while (true) {
                    const { value, done } = await reader.read();
                    if (done) break;
                    
                    const chunk = decoder.decode(value);
                    const lines = chunk.split('\n');
                    
                    for (const line of lines) {
                        if (line.startsWith('data: ')) {
                            try {
                                const data = JSON.parse(line.slice(6));
                                if (data.error) {
                                    console.error('Error:', data.error);
                                    currentBotMessage.querySelector('.message-content').innerHTML = 'Sorry, I encountered an error. Please try again.';
                                    break;
                                } else if (data.content) {
                                    currentMessageContent += data.content;
                                    const contentDiv = currentBotMessage.querySelector('.message-content');
                                    contentDiv.innerHTML = marked.parse(currentMessageContent);
                                    chatMessages.scrollTop = chatMessages.scrollHeight;
                                }
                            } catch (e) {
                                console.error('Error parsing JSON:', e);
                            }
                        }
                    }
                }

            } catch (error) {
                console.error('Error:', error);
                if (currentBotMessage) {
                    currentBotMessage.querySelector('.message-content').innerHTML = 'Sorry, I encountered an error. Please try again.';
                } else {
                    addMessage('Sorry, I encountered an error. Please try again.', 'bot');
                }
            }
        }
    }

    // Create a bot message element
    function createBotMessageElement(initialText) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message';
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.innerHTML = initialText ? marked.parse(initialText) : '';
        
        messageDiv.appendChild(contentDiv);
        return messageDiv;
    }

    // Add message to chat
    function addMessage(message, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.innerHTML = sender === 'bot' ? marked.parse(message) : message;
        
        messageDiv.appendChild(contentDiv);
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Send button click handler
    sendButton.addEventListener('click', sendMessage);

    // File input handler
    fileInput.addEventListener('change', () => {
        filePreview.innerHTML = '';
        Array.from(fileInput.files).forEach(file => {
            const previewItem = document.createElement('div');
            previewItem.className = 'preview-item';
            
            const icon = document.createElement('i');
            icon.className = file.type.startsWith('image/') 
                ? 'fas fa-image' 
                : 'fas fa-file-pdf';
            
            const fileName = document.createElement('span');
            fileName.textContent = file.name;
            
            const removeButton = document.createElement('i');
            removeButton.className = 'fas fa-times remove-file';
            removeButton.onclick = () => previewItem.remove();
            
            previewItem.appendChild(icon);
            previewItem.appendChild(fileName);
            previewItem.appendChild(removeButton);
            filePreview.appendChild(previewItem);
        });
    });

    // Voice recognition setup
    if ('MediaRecorder' in window) {
        voiceButton.addEventListener('click', toggleVoiceRecording);
    } else {
        voiceButton.style.display = 'none';
    }

    async function toggleVoiceRecording() {
        if (!isRecording) {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                mediaRecorder = new MediaRecorder(stream);
                
                mediaRecorder.ondataavailable = (event) => {
                    audioChunks.push(event.data);
                };
                
                mediaRecorder.onstop = () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                    // Here you can implement audio file handling
                    audioChunks = [];
                };
                
                mediaRecorder.start();
                isRecording = true;
                voiceButton.classList.add('recording');
                voiceIndicator.style.display = 'block';
            } catch (err) {
                console.error('Error accessing microphone:', err);
            }
        } else {
            mediaRecorder.stop();
            isRecording = false;
            voiceButton.classList.remove('recording');
            voiceIndicator.style.display = 'none';
        }
    }
});
