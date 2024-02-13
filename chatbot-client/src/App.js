import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { marked } from 'marked';
import DOMPurify from 'dompurify';
import './App.css';


function App() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }

  useEffect(scrollToBottom, [messages]);

  const azureFunctionUrl = 'https://cba-chatbot-prototype.azurewebsites.net/api/chatbot_function';

  const sendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage = { 
      id: Date.now(), 
      text: inputValue, 
      sender: 'user', 
      timestamp: new Date().toLocaleTimeString(),
      sources: [] // User messages do not have sources
    };
    setMessages([...messages, userMessage]);
    
    setInputValue('');

    try {
      const response = await axios.post(azureFunctionUrl, { query: inputValue });
      const botMessage = { 
        id: Date.now(), 
        text: response.data.text,
        sources: response.data.sources,
        sender: 'bot', 
        timestamp: new Date().toLocaleTimeString() 
      };
      setMessages(messages => [...messages, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  const renderMessageContent = (message) => {
    const rawMarkup = marked.parse(message.text);
    const formattedText = formatBoldText(rawMarkup);
    const sanitizedMarkup = DOMPurify.sanitize(formattedText);

    const senderName = message.sender === 'user' ? 'You' : 'Ceba';
  
    return (
      <div>
        {/* Display sender's name */}
        <div className="message-sender">{senderName}</div>

        {/* Render the message as HTML */}
        <div className="message-content" dangerouslySetInnerHTML={{ __html: sanitizedMarkup }}></div>

        {/* Render sources if they exist */}
        {message.sources && message.sources.length > 0 && (
          <div className="message-sources">
            Sources:&nbsp;
            {message.sources.map((source, index) => (
              <span key={index}>
                <a href={source.url} target="_blank" rel="noopener noreferrer">
                  {source.title || source.url}  {/* Fallback to URL if title is not available */}
                </a>
                {index < message.sources.length - 1 ? ' ' : ''}
              </span>
            ))}
          </div>
        )}
      </div>
    );
  };

  function formatBoldText(text) {
    // First replace ‘text’ with <strong>text</strong>
    let formattedText = text.replace(/‘(.*?)’/g, "<strong>‘$1’</strong>");
    // Then replace "text" with <strong>text</strong>
    formattedText = formattedText.replace(/"(.*?)"/g, "<strong>\"$1\"</strong>");
    return formattedText;
  }
  

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h2>Ceba Chat</h2>
      </div>
      <div className="chat-body">
        {messages.map(message => (
          <div key={message.id} className={`message ${message.sender}`}>
            {renderMessageContent(message)}
            <div className="message-timestamp">{message.timestamp}</div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <div className="chat-footer">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' ? sendMessage() : null}
          placeholder="Type a message..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}

export default App;
