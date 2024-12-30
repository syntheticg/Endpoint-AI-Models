# FastAPI with g4f Integration

This is a FastAPI project that integrates the `g4f` library for AI model responses.

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

## Endpoints

- `GET /ai/allmodels` - Returns all available models.
- `GET /ai/{model_name}?text=your_text` - Generates a response based on the selected model and input text.
