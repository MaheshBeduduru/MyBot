Chatbot Project (FastAPI + React)

This project is a proof-of-concept chatbot that uses a FastAPI backend with WebSocket streaming and a React frontend. It supports integration with cloud LLM APIs (OpenAI, Cohere) or local models (GPT4All, Ollama).

🚀 Getting Started

1. Clone the Repository

git clone https://github.com/your-username/chatbot-project.git
cd chatbot-project2. Backend Setup (FastAPI)

Create and Activate Virtual Environment

Windows PowerShell

python -m venv venv
.\venv\Scripts\activate

Linux/macOS

python3 -m venv venv
source venv/bin/activate

Install Dependencies

pip install -r requirements.txt

Environment Variables

Create a .env file in the project root (this file is ignored by Git):

OPENAI_API_KEY=sk-your-openai-key
COHERE_API_KEY=your-cohere-key

Run Backend

uvicorn backend:app --reload

Backend will be available at http://localhost:8000/ws.

3. Frontend Setup (React)

Install Dependencies

npm install

Run Frontend

npm start

Frontend will run on http://localhost:3000 and connect to the backend WebSocket.

📂 Project Structure

project-root/
├── backend/           # FastAPI backend code
├── frontend/          # React frontend code
├── models/            # Local model files (ignored in Git)
├── .env               # API keys (ignored in Git)
├── requirements.txt   # Python dependencies
├── package.json       # Node dependencies
└── README.md          # Documentation

🔑 Notes

Do not commit .env, venv/, node_modules/, or models/.

Update .gitignore to exclude sensitive and generated files.

Use branches for new features and open Pull Requests for collaboration.

🤝 Collaboration Workflow

Pull latest changes before starting work:

git pull origin main

Create a new branch for your feature:

git checkout -b feature/my-feature

Commit and push changes:

git add .
git commit -m "Added streaming support"
git push origin feature/my-feature

Open a Pull Request for review and merge.

📑 Supported Models

OpenAI: gpt-3.5-turbo, gpt-4

Cohere: command-a-03-2025, command-light

Local: GPT4All, Ollama

📖 License

This project is for educational and proof-of-concept purposes.