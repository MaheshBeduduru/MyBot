import React, { useState, useEffect } from "react";

function App() {
  const [socket, setSocket] = useState(null);
  const [msg, setMsg] = useState("");
  const [reply, setReply] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    // Connect to WebSocket server
    const ws = new WebSocket("ws://localhost:8000/ws");
    
    ws.onopen = () => {
      console.log("Connected to chatbot server");
      setError("");
    };
    
    ws.onmessage = (event) => {
      const data = event.data;
      
      // Handle end-of-message marker
      if (data === "[END]") {
        setIsLoading(false);
        return;
      }
      
      // Handle error messages
      if (data.startsWith("[ERROR]")) {
        setError(data.replace("[ERROR]", "").trim());
        setIsLoading(false);
        return;
      }
      
      // Append word to reply (with space separator)
      setReply((prev) => (prev ? prev + " " + data : data));
    };
    
    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
      setError("Connection error. Make sure the backend server is running.");
      setIsLoading(false);
    };
    
    ws.onclose = () => {
      console.log("Disconnected from server");
    };
    
    setSocket(ws);
    
    return () => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.close();
      }
    };
  }, []);

  const sendMessage = () => {
    if (socket && msg.trim()) {
      setIsLoading(true);
      setReply(""); // reset reply for new message
      setError("");
      socket.send(msg);
    }
  };

  // Handle Enter key press
  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  };

  return (
    <div className="container">
      <div className="chat-box">
        <h1>🤖 Chatbot POC (WebSocket)</h1>
        
        <div className="input-group">
          <input
            type="text"
            value={msg}
            onChange={(e) => setMsg(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
            disabled={isLoading}
          />
          <button onClick={sendMessage} disabled={isLoading}>
            {isLoading ? "Waiting..." : "Send"}
          </button>
        </div>
        
        {error && <div className="error-message">{error}</div>}
        
        <div className="response-area">
          <div className="label">Bot Response:</div>
          <p className={`bot-reply ${isLoading ? "loading" : ""}`}>
            {reply || (isLoading ? "Generating response..." : "Responses will appear here")}
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;
