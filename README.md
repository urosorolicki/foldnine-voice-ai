# FoldNine Voice AI

A public **voice assistant demo** using FastAPI, Ollama, browser speech recognition and browser text-to-speech.

**Status:** Newly created demonstration; not a recovered historical repository. The complete voice flow has not yet been integration-tested. Browser speech recognition may rely on browser-vendor services.

## Architecture

Microphone → Browser SpeechRecognition → FastAPI → Ollama → Browser SpeechSynthesis → Speaker

## Quick start

```bash
docker compose up --build -d
docker compose exec ollama ollama pull llama3.2:3b
```

Open http://localhost:8000. Text input works even without microphone support.

## Test

```bash
pip install -r requirements.txt
pytest -q
```

## API

- `GET /health` — liveness
- `POST /api/chat` — `{"message":"Hello","history":[]}`

## Limitations

- Browser voice support varies; recognition may not run locally.
- No authentication, rate limiting or streaming.
- For fully self-hosted voice, add Whisper STT and Piper TTS.
- This demo is not production-hardened.

MIT licensed.
