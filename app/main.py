import os

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

app = FastAPI(title="FoldNine Voice AI", version="0.1.0")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434").rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    history: list[dict[str, str]] = Field(default_factory=list, max_length=12)


@app.get("/")
def index():
    return FileResponse("app/static/index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/chat")
async def chat(request: ChatRequest):
    messages = [{"role": "system", "content": "You are a concise helpful voice assistant."}]
    for item in request.history:
        if item.get("role") in ("user", "assistant") and isinstance(item.get("content"), str):
            messages.append({"role": item["role"], "content": item["content"][:4000]})
    messages.append({"role": "user", "content": request.message})
    try:
        async with httpx.AsyncClient(timeout=90) as client:
            response = await client.post(
                f"{OLLAMA_URL}/api/chat",
                json={"model": OLLAMA_MODEL, "messages": messages, "stream": False},
            )
            response.raise_for_status()
            return {"reply": response.json()["message"]["content"]}
    except (httpx.HTTPError, KeyError, ValueError) as exc:
        raise HTTPException(status_code=502, detail="Ollama unavailable or invalid response") from exc
