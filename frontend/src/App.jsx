import { useState, useRef, useEffect } from 'react'
import './App.css'

function App() {
  const [messages, setMessages] = useState([
    { id: 1, text: 'Hello! 👋 How can I help you today?', sender: 'bot', timestamp: new Date() }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const sendMessage = async (e) => {
    e.preventDefault()
    
    if (!input.trim()) return

    // Add user message to chat
    const userMessage = {
      id: messages.length + 1,
      text: input,
      sender: 'user',
      timestamp: new Date()
    }
    
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      // Call backend API
      const response = await fetch(`http://localhost:8000/search?query=${encodeURIComponent(input)}&k=2`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      
      // Format results as bot message
      const resultText = data.results && data.results.length > 0
        ? data.results.join('\n\n')
        : 'No relevant information found for your query.'
      
      const botMessage = {
        id: messages.length + 2,
        text: resultText,
        sender: 'bot',
        timestamp: new Date()
      }
      
      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      console.error('Error:', error)
      const errorMessage = {
        id: messages.length + 2,
        text: '❌ Sorry, I encountered an error. Please try again.',
        sender: 'bot',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="chatbot-container">
      <div className="chatbot-header">
        <h1>💬 AI Chatbot</h1>
        <p>Ask me anything!</p>
      </div>

      <div className="chatbot-messages">
        {messages.map((msg) => (
          <div key={msg.id} className={`message message-${msg.sender}`}>
            <div className="message-content">
              {msg.text}
            </div>
            <div className="message-time">
              {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </div>
          </div>
        ))}
        {loading && (
          <div className="message message-bot">
            <div className="message-content">
              <span className="typing-indicator">
                <span></span><span></span><span></span>
              </span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={sendMessage} className="chatbot-input-form">
        <div className="input-wrapper">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message here..."
            disabled={loading}
            className="message-input"
          />
          <button 
            type="submit" 
            disabled={loading || !input.trim()}
            className="send-button"
          >
            {loading ? '⏳' : '➤'}
          </button>
        </div>
      </form>
    </div>
  )
}

export default App
