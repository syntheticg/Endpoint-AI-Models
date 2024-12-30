from fastapi import FastAPI, HTTPException
from typing import Optional
import g4f

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

@app.get("/ai/allmodels")
async def get_all_models():
    return {"models": models}

@app.get("/ai/{model_name}")
async def get_model_response(model_name: str, text: Optional[str] = ""):
    if model_name not in models:
        raise HTTPException(status_code=404, detail="Model not found")

    if not text:
        raise HTTPException(status_code=400, detail="Text query is required")

    try:
        provider = g4f.Provider.Forefront  # Replace with your desired provider

        response = g4f.ChatCompletion.create(
            model=model_name,
            messages=[{"role": "user", "content": text}],
            provider=provider,
        )
        return {
            "model": models[model_name],
            "input_text": text,
            "generated_text": response,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")
