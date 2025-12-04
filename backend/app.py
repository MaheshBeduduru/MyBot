from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
dotenv_path = "c:/Mahesh/MyBot/backend/.env"
if Path(dotenv_path).exists():
    load_dotenv(dotenv_path=dotenv_path)
    print("Environment variables loaded from .env file.")
else:
    print(f".env file not found at {dotenv_path}")

# HTTP client for HF Inference API
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
print(f"HF_API_TOKEN: {HF_API_TOKEN}")  # Debugging line
if not HF_API_TOKEN:
    raise ValueError("HF_API_TOKEN environment variable is not set. Please configure it.")

try:
    import httpx
except ImportError:
    raise ImportError("httpx library is required. Install it with 'pip install httpx'.")

app = FastAPI()

# Add CORS middleware to allow requests from React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint that receives messages and streams back generated responses.
    Responses are streamed word-by-word for real-time display.
    """
    await websocket.accept()
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            
            if not data.strip():
                await websocket.send_text("[ERROR] Empty message")
                continue
            
            try:
                # Use Hugging Face Inference API with detailed logging
                headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
                payload = {"inputs": data, "parameters": {"max_new_tokens": 100, "do_sample": True}}
                print(f"Request Headers: {headers}")
                print(f"Request Payload: {payload}")
                async with httpx.AsyncClient(timeout=60.0) as client:
                    resp = await client.post(
                        "https://api-inference.huggingface.co/models/facebook/opt-125m",  # Updated endpoint and model
                        headers=headers,
                        json=payload,
                    )
                    print(f"HF API Response: {resp.status_code}, {resp.text}")  # Debugging line
                    if resp.status_code != 200:
                        raise ValueError(f"API Error: {resp.status_code}, {resp.text}")
                    json_resp = resp.json()
                    if isinstance(json_resp, list):
                        reply = json_resp[0].get("generated_text", "")
                    else:
                        reply = json_resp.get("generated_text", "")

                # Stream reply word-by-word
                words = reply.split()
                for word in words:
                    await websocket.send_text(word)
                    await asyncio.sleep(0.05)

                # Send end-of-message marker
                await websocket.send_text("[END]")

            except Exception as e:
                print(f"Error during API call: {e}")
                await websocket.send_text(f"[ERROR] {str(e)}")
    
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Chatbot API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
