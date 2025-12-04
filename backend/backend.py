import os
import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import cohere

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

co = cohere.Client("tRXVd5jFEhAR0MQNonHwkgkCcHV0QaRQfjtb0Q8o")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            user_msg = await websocket.receive_text()
            print(f"User: {user_msg}")

            # Use a currently supported model
            stream = co.chat_stream(
                model="command-a-03-2025",
                message=user_msg
            )

            for event in stream:
                if event.event_type == "text-generation":
                    await websocket.send_text(event.text)

            await websocket.send_text("[END]")

    except Exception as e:
        print("Error:", e)
        await websocket.close()

if __name__ == "__main__":
    uvicorn.run("backend:app", host="0.0.0.0", port=8000, reload=True)