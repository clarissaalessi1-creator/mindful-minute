
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Mindful Minute")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "Welcome to Mindful Minute",
        "prototype": True
    }

@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "application": "Mindful Minute"
    }
