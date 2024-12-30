from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from g4f.client import Client

app = FastAPI()

# Data model list
models = {
    "gpt-4o-mini": {
        "name": "GPT-4O Mini",
        "description": "Optimized GPT-4 Mini model",
        "endpoint": "/ai/gpt-4o-mini?text=",
    },
    "gpt-4": {
        "name": "GPT-4",
        "description": "Powerful GPT-4 model",
        "endpoint": "/ai/gpt-4?text=",
    },
}

# Initialize client
client = Client()

async def get_model_response(model_name: str, text: str) -> str:
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": text}],
            web_search=False
        )
        return response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

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
