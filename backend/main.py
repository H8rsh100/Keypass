import os
import json
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional

from backend.hasher import hash_password
from backend.benchmark import run_benchmark

app = FastAPI(title="Keypass API", description="Educational Password Cracking Demonstrator")

# Request Models
class HashRequest(BaseModel):
    password: str
    algorithm: str

class BenchmarkRequest(BaseModel):
    password: str
    algorithm: str

# API Routes
@app.post("/api/hash")
def api_hash(payload: HashRequest):
    try:
        hashed = hash_password(payload.password, payload.algorithm)
        return {"hash": hashed, "password": payload.password, "algorithm": payload.algorithm}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/benchmark")
def api_benchmark(payload: BenchmarkRequest):
    try:
        # Prevent benchmarking bcrypt with brute force if it is too slow
        # but run_benchmark uses min(len(password), 4) and 2.0s limit, so it's safe.
        results = run_benchmark(payload.password, payload.algorithm)
        return results
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# WebSocket Route for Live Crack / Precompute Progress
@app.websocket("/api/ws/crack")
async def websocket_crack(websocket: WebSocket):
    await websocket.accept()
    try:
        # Wait for start configuration message
        message = await websocket.receive_text()
        config = json.loads(message)
        
        action = config.get("action") # "dictionary", "brute_force", "precompute"
        algorithm = config.get("algorithm", "sha256")
        
        if action == "precompute":
            from backend.rainbow_table import precompute_rainbow_table
            for progress in precompute_rainbow_table():
                await websocket.send_json({"type": "precompute", "data": progress})
                await asyncio.sleep(0.0001)
            return

        target_hash = config.get("target_hash")
        if not target_hash:
            await websocket.send_json({"error": "Missing target_hash"})
            return

        if action == "dictionary":
            from backend.dictionary_attack import dictionary_attack
            for progress in dictionary_attack(target_hash, algorithm):
                await websocket.send_json({"type": "dictionary", "data": progress})
                await asyncio.sleep(0.0001)
                
        elif action == "brute_force":
            charset_types = config.get("charset_types", ["lowercase"])
            max_length = config.get("max_length", 4)
            from backend.brute_force import brute_force_attack
            for progress in brute_force_attack(
                target_hash=target_hash,
                algorithm=algorithm,
                charset_types=charset_types,
                max_length=max_length
            ):
                await websocket.send_json({"type": "brute_force", "data": progress})
                await asyncio.sleep(0.0001)
        else:
            await websocket.send_json({"error": f"Unknown action: {action}"})

    except WebSocketDisconnect:
        pass
    except Exception as e:
        try:
            await websocket.send_json({"error": str(e)})
        except Exception:
            pass
    finally:
        try:
            await websocket.close()
        except Exception:
            pass

# Serve static frontend files
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
os.makedirs(FRONTEND_DIR, exist_ok=True)
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
