import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from gpt4all import GPT4All

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Make sure you downloaded the model into ./models
model = GPT4All("gpt4all-falcon-q4_0.bin", model_path="models")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            user_msg = await websocket.receive_text()
            print(f"User: {user_msg}")

            response = ""
            for token in model.generate(f"User: {user_msg}\nBot:", streaming=True):
                await websocket.send_text(token)
                response += token

            await websocket.send_text("[END]")

    except Exception as e:
        print("Error:", e)
        await websocket.close()

if __name__ == "__main__":
    uvicorn.run("backend:app", host="0.0.0.0", port=8000, reload=True)