from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from transformers import pipeline

app = FastAPI(title="Financial Sentiment Analysis API (FinBERT)")

MODEL_NAME = "ProsusAI/finbert"

# Load ProsusAI/finbert once on startup
try:
    classifier = pipeline("text-classification", model=MODEL_NAME)
except Exception as e:
    classifier = None
    startup_error = str(e)

class FinancialTextInput(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="English financial news headline or sentence to classify",
        examples=["Stocks rallied and the British pound gained."]
    )

@app.get("/")
def read_root():
    return {
        "system": "Financial Text Classification API",
        "model": MODEL_NAME,
        "model_url": f"https://huggingface.co/{MODEL_NAME}",
        "labels": ["positive", "negative", "neutral"],
        "endpoints": {
            "GET /": "System description and available endpoints",
            "GET /health": "Check operational status and model readiness",
            "POST /predict": "Classify financial text sentiment"
        }
    }

@app.get("/health")
def health_check():
    if classifier is None:
        raise HTTPException(
            status_code=503, 
            detail=f"Model failed to load: {startup_error}"
        )
    return {"status": "healthy", "model": MODEL_NAME, "model_loaded": True}

@app.post("/predict")
def predict_sentiment(payload: FinancialTextInput):
    if classifier is None:
        raise HTTPException(status_code=503, detail="Model is not loaded.")

    cleaned_text = payload.text.strip()
    if not cleaned_text:
        raise HTTPException(
            status_code=400, 
            detail="Input text cannot be empty or whitespace only."
        )

    try:
        # top_k=None returns scores for all 3 labels (positive, negative, neutral) sorted highest first
        results = classifier(cleaned_text, top_k=None)
        top_prediction = results[0]

        return {
            "input_text": cleaned_text,
            "predicted_label": top_prediction["label"],
            "confidence": round(top_prediction["score"], 4),
            "all_scores": {
                item["label"]: round(item["score"], 4) for item in results
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")