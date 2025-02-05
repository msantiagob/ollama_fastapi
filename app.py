from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.responses import RedirectResponse
import requests
import json
import time

app = FastAPI()

# Crear un router
api_router = APIRouter(prefix="/api8000")

@api_router.get("/")
def read_root():
    return {"message": "Bienvenido a la API ollama"}

@api_router.post("/generate")
async def generate_text(prompt: str):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "phi",
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_keep": 5,
            "seed": 42,
            "num_predict": 100,
            "top_k": 20,
            "top_p": 0.9,
            "tfs_z": 0.5,
            "typical_p": 0.7,
            "repeat_last_n": 33,
            "temperature": 0.8,
            "repeat_penalty": 1.2,
            "presence_penalty": 1.5,
            "frequency_penalty": 1.0,
            "mirostat": 1,
            "mirostat_tau": 0.8,
            "mirostat_eta": 0.6,
            "penalize_newline": True,
            "numa": False,
            "num_ctx": 1024,
            "num_batch": 2,
            "num_gpu": 1,
            "main_gpu": 0,
            "low_vram": False,
            "f16_kv": True,
            "vocab_only": False,
            "use_mmap": True,
            "use_mlock": False,
            "num_thread": 8
        }
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with Ollama: {str(e)}")

# Manejador para errores 404
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    if exc.status_code == 404:
        return RedirectResponse(url="/api8000/docs")
    return await request.app.default_http_exception_handler(request, exc)

# Incluir el router en la aplicación
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
