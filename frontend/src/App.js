import React, { useState, useEffect } from 'react';

function App() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');
  const [messages, setMessages] = useState([]);

  const fetchMessages = async () => {
    try {
      const res = await fetch('http://20.215.192.139:5001/api/data');
      if (res.ok) {
        const data = await res.json();
        setMessages(data);
      } else {
        console.error('Failed to fetch messages.');
      }
    } catch (error) {
      console.error('Error fetching messages:', error);
    }
  };

  useEffect(() => {
    fetchMessages();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      console.log('Sending message:', message); // Debug log
      const res = await fetch('http://20.215.192.139:5001/api/send', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        mode: 'cors',
        body: JSON.stringify({ message: message }),
      });
      
      console.log('Response status:', res.status); // Debug log
      
      if (res.ok) {
        const data = await res.json();
        console.log('Response data:', data); // Debug log
        setResponse(data.status || 'Message sent successfully!');
        setMessage('');
        await fetchMessages(); // Refresh messages list
      } else {
        const errorData = await res.json();
        setResponse(`Failed to send the message: ${errorData.error || res.statusText}`);
      }
    } catch (error) {
      console.error('Error details:', error); // Debug log
      setResponse(`Error: ${error.message}`);
    }
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial' }}>
      <h1>Frontend Communication</h1>
      <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
        <label>
          <strong>Message to Kafka:</strong>
        </label>
        <br />
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Enter your message"
          style={{ padding: '10px', width: '300px', marginTop: '10px' }}
        />
        <br />
        <button type="submit" style={{ marginTop: '10px', padding: '10px' }}>
          Send Message
        </button>
      </form>
      {response && (
        <div>
          <strong>Response:</strong>
          <p>{response}</p>
        </div>
      )}
      <h2>Messages from Database:</h2>
      {messages.length > 0 ? (
        <ul>
          {messages.map((msg, index) => (
            <li key={index}>
              <strong>ID:</strong> {msg.id}, <strong>Data:</strong> {msg.data}
            </li>
          ))}
        </ul>
      ) : (
        <p>No messages available.</p>
      )}
    </div>
  );
}

export default App;
