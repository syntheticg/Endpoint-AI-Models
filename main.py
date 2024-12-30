from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from g4f.client import Client
from g4f.Provider import OpenaiChat, DeepAi

app = FastAPI()

# Data model list
models = {
    "gpt-4": {
        "name": "GPT-4",
        "description": "Powerful GPT-4 model",
        "endpoint": "/ai/gpt-4?text=",
    },
    "gpt-3.5": {
        "name": "GPT-3.5",
        "description": "Lightweight GPT-3.5 model",
        "endpoint": "/ai/gpt-3.5?text=",
    },
}

# List provider fallback
providers = [OpenaiChat, DeepAi]

async def get_model_response(model_name: str, text: str) -> dict:
    for provider in providers:
        try:
            client = Client(provider=provider)
            response = client.create_chat_completion(
                model=model_name,
                messages=[{"role": "user", "content": text}],
            )
            return response
        except Exception as e:
            continue  # Coba provider berikutnya jika gagal
    raise HTTPException(status_code=500, detail="All providers failed.")

@app.get("/ai/allmodels")
async def get_all_models():
    return {"models": models}

@app.get("/ai/{model_name}")
async def ai_endpoint(model_name: str, text: Optional[str] = Query(None)):
    if model_name not in models:
        raise HTTPException(status_code=404, detail="Model not found")
    if not text:
        raise HTTPException(status_code=400, detail="Text query is required")
    try:
        response = await get_model_response(model_name, text)
        return {
            "model": models[model_name],
            "input_text": text,
            "generated_text": response,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
