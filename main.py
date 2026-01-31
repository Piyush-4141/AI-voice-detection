from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Optional
import base64
import random
import os

app = FastAPI()

API_KEY = os.getenv("API_KEY", "test123")

# -------- Request Schema --------
class VoiceRequest(BaseModel):
    language: str
    audio_format: str
    audio_base64: str

# -------- API Endpoint --------
@app.post("/detect-voice")
def detect_voice(
    data: VoiceRequest,
    x_api_key: str = Header(None)
):
    # ---- API Key Check ----
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # ---- Decode Base64 Audio ----
    try:
        audio_bytes = base64.b64decode(data.audio_base64)
    except:
        raise HTTPException(status_code=400, detail="Invalid Base64 audio")

    # ---- Dummy AI Logic ----
    confidence = round(random.uniform(0.65, 0.9), 2)
    classification = "AI-generated" if confidence > 0.75 else "Human-generated"

    return {
        "classification": classification,
        "confidence": confidence,
        "explanation": "Synthetic voice patterns detected"
    }

# -------- Health Check --------
@app.get("/")
def home():
    return {"status": "API is running"}
