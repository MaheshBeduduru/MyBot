# Chatbot POC (WebSocket + Streaming)

A full-stack proof of concept for a real-time chatbot using FastAPI backend with WebSocket streaming and React frontend.

## 🎯 Features

- **Real-time WebSocket Communication** - Instant message delivery between client and server
- **Streaming Responses** - Bot responses stream word-by-word for dynamic UI updates
- **AI-Powered** - Uses Hugging Face Transformers (GPT-2) for text generation
- **Error Handling** - Graceful error messages and connection management
- **Responsive UI** - Mobile-friendly interface with gradient design
- **Enter Key Support** - Send messages with Enter key

## 📁 Project Structure

```
MyBot/
├── backend/
│   ├── app.py              # FastAPI WebSocket server
│   └── requirements.txt     # Python dependencies
├── src/
│   ├── App.js              # React component with WebSocket client
│   └── index.js            # React entry point
├── public/
│   └── index.html          # HTML template
├── package.json            # Node.js dependencies
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ (for backend)
- Node.js 14+ (for frontend)
- pip (Python package manager)
- npm (Node package manager)

### Backend Setup (Python)

1. **Open a terminal in the `backend/` directory:**
   ```powershell
   cd backend
   ```

2. **Create a virtual environment (recommended):**
   ```powershell
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows (PowerShell):
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - On Windows (Command Prompt):
     ```cmd
     venv\Scripts\activate.bat
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```
   
   ⚠️ **Note:** First installation may take 5-10 minutes as it downloads the GPT-2 model (~500MB)

5. **Run the FastAPI server:**
   ```powershell
   python app.py
   ```
   
   You should see:
   ```
   Loading model... This may take a moment on first run.
   Model loaded successfully!
   INFO:     Uvicorn running on http://0.0.0.0:8000
   ```

### Frontend Setup (React)

1. **Open a new terminal in the root directory (MyBot/):**
   ```powershell
   cd ..
   ```

2. **Install Node.js dependencies:**
   ```powershell
   npm install
   ```

3. **Start the React development server:**
   ```powershell
   npm start
   ```
   
   The browser should automatically open to `http://localhost:3000`

## 💬 How to Use

1. Ensure both the **backend server** (on port 8000) and **frontend** (on port 3000) are running
2. Type a message in the input field
3. Click **Send** or press **Enter**
4. Watch the bot response stream in real-time, word-by-word
5. The chat area clears automatically for the next message

## 🔧 How It Works

### Backend Flow
```
User Message → WebSocket → FastAPI Server 
    → GPT-2 Model Generates Text
    → Response Streamed Word-by-Word
    → Words Sent Back via WebSocket → React Frontend
```

### Frontend Flow
```
User Input → Send Message via WebSocket
    → Receive Words → Accumulate in State
    → Real-time Display Update
    → Show [END] Marker → Ready for Next Message
```

## 📝 Configuration

### Change the AI Model
Edit `backend/app.py`, line ~17:
```python
generator = pipeline("text-generation", model="gpt2")  # Change "gpt2" to another model
```

Popular alternatives:
- `"distilgpt2"` - Faster, smaller model
- `"gpt2-medium"` - Better quality responses
- `"EleutherAI/gpt-neo-125m"` - More advanced

### Adjust Response Length
Edit `backend/app.py`, line ~42:
```python
outputs = generator(data, max_length=100, do_sample=True)  # Change max_length
```

### Change Server Port
Edit `backend/app.py`, line ~63:
```python
uvicorn.run(app, host="0.0.0.0", port=8000)  # Change port
```

Update the WebSocket URL in `src/App.js`, line ~13:
```javascript
const ws = new WebSocket("ws://localhost:8000/ws");  // Update port
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **"Cannot connect to server"** | Make sure backend is running on port 8000 |
| **"Module not found" (Python)** | Activate virtual environment and run `pip install -r requirements.txt` |
| **Slow first request** | First model load takes time. Subsequent requests are faster |
| **Port 8000 already in use** | Kill the process on that port or change the port number |
| **WebSocket connection error** | Check backend server is running: `http://localhost:8000` |

## 📦 Dependencies

### Backend
- **FastAPI** - Modern web framework for building APIs
- **Uvicorn** - ASGI server to run FastAPI
- **Transformers** - Hugging Face library for NLP models
- **Torch** - Deep learning framework

### Frontend
- **React** - UI library
- **React DOM** - React rendering engine
- **React Scripts** - Build and development tools

## 🔐 Notes

- This is a POC - not optimized for production
- Large language models consume significant system resources
- Consider using GPU for faster inference
- Error handling includes disconnection management

## 📚 Learn More

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/)
- [React Documentation](https://react.dev/)

---

**Built with ❤️ as a chatbot proof of concept**
