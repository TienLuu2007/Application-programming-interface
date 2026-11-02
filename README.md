# Application-programming-interface

## **Student**
- **Full Name:** Lưu Minh Tiến
- **Student ID:** 25127242

## **Model** 
- **Name:** `ProsusAI/finbert`
- **Hugging Face Link:** [https://huggingface.co/ProsusAI/finbert](https://huggingface.co/ProsusAI/finbert)

## **Description** 
This project implements a RESTful Web API using **FastAPI** to serve the `ProsusAI/finbert` model from Hugging Face. FinBERT is a pre-trained NLP model based on BERT, specifically fine-tuned on financial communication (the Financial PhraseBank dataset) to analyze the sentiment of financial text.

The API accepts English financial sentences, earnings snippets, or market headlines and classifies them into three sentiment categories:
- `positive`
- `negative`
- `neutral`

In addition to returning the primary predicted label and its confidence score, the API provides the full probability distribution across all three classes, along with input validation and error handling for invalid or empty requests.

## **Installing the required dependencies**
```bash
pip install -r requirements.txt
```

## **Running instruction** 
Start the FastAPI server:
```bash
uvicorn main:app --reload
```

## **API call instruction**
### Automated Testing with `requests`
While the FastAPI server is running in the first terminal, open a second terminal and run the test script:
```bash
python test_api.py
```

### Endpoint Reference

#### 1. `GET /`
Returns metadata about the API, the underlying Hugging Face model, and available endpoints.

- **Example Request:**
  ```bash
  curl -X GET [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
  ```
- **Example Response (`200 OK`):**
  ```json
  {
    "system": "Financial Text Classification API",
    "model": "ProsusAI/finbert",
    "model_url": "[https://huggingface.co/ProsusAI/finbert](https://huggingface.co/ProsusAI/finbert)",
    "labels": ["positive", "negative", "neutral"],
    "endpoints": {
      "GET /": "System description and available endpoints",
      "GET /health": "Check operational status and model readiness",
      "POST /predict": "Classify financial text sentiment"
    }
  }
  ```

#### 2. `GET /health`
Verifies that the FastAPI server is operational and the FinBERT model is loaded in memory.

- **Example Request:**
  ```bash
  curl -X GET [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)
  ```
- **Example Response (`200 OK`):**
  ```json
  {
    "status": "healthy",
    "model": "ProsusAI/finbert",
    "model_loaded": true
  }
  ```

#### 3. `POST /predict`
Receives an English financial text string, invokes `ProsusAI/finbert`, and returns the classification result in JSON format.

- **Example Request 1 (Positive Sentiment):**
  ```bash
  curl -X POST [http://127.0.0.1:8000/predict](http://127.0.0.1:8000/predict) \
       -H "Content-Type: application/json" \
       -d '{"text": "Stocks rallied and the British pound gained after strong quarterly earnings."}'
  ```
- **Example Response 1 (`200 OK`):**
  ```json
  {
    "input_text": "Stocks rallied and the British pound gained after strong quarterly earnings.",
    "predicted_label": "positive",
    "confidence": 0.9482,
    "all_scores": {
      "positive": 0.9482,
      "neutral": 0.0329,
      "negative": 0.0189
    }
  }
  ```

- **Example Request 2 (Negative Sentiment):**
  ```bash
  curl -X POST [http://127.0.0.1:8000/predict](http://127.0.0.1:8000/predict)
       -H "Content-Type: application/json"
       -d '{"text": "Operating profit fell 25% due to rising supply chain costs and weak demand."}'
  ```
- **Example Response 2 (`200 OK`):**
  ```json
  {
    "input_text": "Operating profit fell 25% due to rising supply chain costs and weak demand.",
    "predicted_label": "negative",
    "confidence": 0.9714,
    "all_scores": {
      "negative": 0.9714,
      "neutral": 0.0185,
      "positive": 0.0101
    }
  }
  ```

- **Example Request 3 (Error Handling for Empty Input):**
  ```bash
  curl -X POST [http://127.0.0.1:8000/predict](http://127.0.0.1:8000/predict) \
       -H "Content-Type: application/json" \
       -d '{"text": "   "}'
  ```
- **Example Response 3 (`400 Bad Request`):**
  ```json
  {
    "detail": "Input text cannot be empty or whitespace only."
  }
  ```

## **Demonstration Video**
- **Video Link:** [25127242_LuuMinhTien](https://drive.google.com/file/d/14kQs2CL5QG6d2_FO1tEdPb9V4K34sKku/view?usp=sharing)