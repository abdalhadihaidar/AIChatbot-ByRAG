import React, { useState, useEffect, useRef } from 'react';
import './FloatingButton.css'; // Assuming the CSS is in this file
import axios from 'axios';

const FloatingButton = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [prompt, setPrompt] = useState('');
    const [messages, setMessages] = useState([]);
    const messagesEndRef = useRef(null);  // Create a reference to the bottom of the chat

    // Scroll to the bottom of the chat messages when a new message is added
    const scrollToBottom = () => {
        if (messagesEndRef.current) {
            messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);  // Whenever the messages array changes, scroll to bottom

    const toggleChatbot = () => {
        setIsOpen(!isOpen);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (prompt.trim()) {
            const userMessage = { sender: 'user', text: prompt };
            setMessages((prevMessages) => [...prevMessages, userMessage]);

            try {
                // Send the prompt to the backend (replace '/query' with your actual backend endpoint)
                const response = await axios.post('http://localhost:5000/query', { query: prompt });

                // Access the 'answer' field from the backend's response instead of 'reply'
                const botMessage = { sender: 'bot', text: response.data.results.answer || 'No response available.' };
                setMessages((prevMessages) => [...prevMessages, botMessage]);
            } catch (error) {
                console.error('Error sending prompt:', error);
                const botErrorMessage = { sender: 'bot', text: 'Error: Unable to get a response.' };
                setMessages((prevMessages) => [...prevMessages, botErrorMessage]);
            }

            setPrompt('');
        }
    };

    return (
        <div>
            {/* Floating Button */}
            <button className="floating-btn" onClick={toggleChatbot}>
                💬 Chat
            </button>

            {/* Chatbot Window */}
            {isOpen && (
                <div className="chatbot-window">
                    <div className="chatbot-header">
                        <h3>Chatbot</h3>
                        <button className="close-btn" onClick={toggleChatbot}>✖</button>
                    </div>
                    <div className="chatbot-body">
                        {/* Scrollable Chat Messages */}
                        <div className="chat-messages">
                            {messages.map((msg, index) => (
                                <div key={index} className={msg.sender === 'user' ? 'user-message' : 'bot-message'}>
                                    <p>{msg.text}</p>
                                </div>
                            ))}
                            <div ref={messagesEndRef} /> {/* This will track the bottom of the chat */}
                        </div>
                        {/* Input Field */}
                        <form onSubmit={handleSubmit} className="chat-input-form">
                            <input
                                type="text"
                                value={prompt}
                                onChange={(e) => setPrompt(e.target.value)}
                                placeholder="Type your message..."
                                required
                            />
                            <button type="submit">Send</button>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default FloatingButton;
