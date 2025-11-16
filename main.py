from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import os
import uvicorn
import numpy as np
import re
from scipy.sparse import hstack
from datetime import datetime  # new added for timestamp in history
import json              
from fastapi import HTTPException     
import secrets # new added for unique IDs in history

BASE_DIR = os.path.dirname(__file__)
model = joblib.load(os.path.join(BASE_DIR, "spam_model.joblib"))
vectorizer = joblib.load(os.path.join(BASE_DIR, "tfidf_vectorizer.joblib"))
scaler = joblib.load(os.path.join(BASE_DIR, "scaler.joblib"))
HISTORY_FILE = os.path.join(BASE_DIR, "history.json")  # history file path

if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)


def save_history():
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

# Load history
try:
    with open(HISTORY_FILE, "r") as f:
        data = f.read().strip()

        if not data:
            history = []
            save_history()  # rewrite clean JSON
        else:
            history = json.loads(data)

except Exception:
    history = []
    save_history()


# pydantic model for input data validation
class EmailInput(BaseModel):
    text: str

# pydantic model for output data
class PredictionOutput(BaseModel):
    prediction: str
    confidence: float
    id: str
    timestamp: str



URL_PATTERN = re.compile(r"http[s]?://\S+|www\.\S+")
EMAIL_PATTERN = re.compile(r"\b[\w\.-]+@[\w\.-]+\.\w+\b")
PHONE_PATTERN = re.compile(r"\b\d{3}-\d{3}-\d{4}\b")
MONEY_PATTERN = re.compile(r"\$+\s*\d[\d\s,]*(?:[.]\d+)?")

def clean_text(s: str) -> str:
    s = str(s).lower()
    s = re.sub(r"^subject:\s*", "", s)
    s = re.sub(r"\s*([^\w\s])\s*", r"\1", s)
    s = URL_PATTERN.sub(" URL ", s)
    s = PHONE_PATTERN.sub(" PHONENUMBER ", s)
    s = EMAIL_PATTERN.sub(" EMAIL ", s)
    s = MONEY_PATTERN.sub(" MONEY ", s)
    s = re.sub(r"@\w+", "", s)
    s = re.sub(r"[^a-zA-Z0-9\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def count_special_chars(text):
    return len(re.findall(r'[!$%&*@#_?]', str(text)))


app = FastAPI()


origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

    
# API endpoint for spam prediction

# Predict spam
@app.post("/predict/", response_model=PredictionOutput)
def predict_spam(data: EmailInput):
    try:
        text = data.text

       #require at least 10 words

        if len(text.strip().split()) < 10:
            raise HTTPException(
                status_code=400,
                detail="Input text must contain at least 10 words."
            )

        cleaned = clean_text(text)
        char_len = len(cleaned)
        word_len = len(cleaned.split())
        special_char_count = count_special_chars(text)
        has_url = int("url" in cleaned.lower())

        text_tfidf = vectorizer.transform([cleaned])
        numeric_features = np.array([[char_len, word_len, special_char_count, has_url]])
        numeric_scaled = scaler.transform(numeric_features)

        features = hstack([text_tfidf, numeric_scaled])

        prediction = model.predict(features)[0]
        probs = model.predict_proba(features)[0]
        label = "spam" if prediction == 1 else "ham"
        confidence = round(float(probs[prediction] * 100), 2)

        entry = {
            "id": secrets.token_hex(4),
            "timestamp": datetime.now().isoformat(),
            "text": text,
            "prediction": label,
            "confidence": confidence
        }

        history.append(entry)
        save_history()

        return PredictionOutput(
            prediction=label,
            confidence=confidence,
            id=entry["id"],
            timestamp=entry["timestamp"]
        )
    except Exception as e:
        raise HTTPException(500, detail=f"Prediction failed: {str(e)}")


#endpoint to get hisrory
@app.get("/history/")
def get_history():
    try:
        return list(reversed(history))
    except Exception as e:
        raise HTTPException(500, detail=f"Failed to fetch history: {str(e)}")
    
# delete by index
@app.delete("/history/delete/{index}")
def delete_history(index: int):
    try:
        removed = history.pop(index)
        save_history()
        return {"message": "History entry deleted", "deleted": removed}

    except IndexError:
        raise HTTPException(404, detail="Index out of range, nothing deleted")

    except Exception as e:
        raise HTTPException(500, detail=f"Failed to delete entry: {str(e)}")
    
# delete by unique ID
@app.delete("/history/delete/id/{entry_id}")
def delete_history_by_id(entry_id: str):
    try:
        for i, item in enumerate(history):
            if item["id"] == entry_id:
                removed = history.pop(i)
                save_history()
                return {"message": "History entry deleted", "deleted": removed}

        raise HTTPException(404, detail="ID not found")
    except Exception as e:
        raise HTTPException(500, detail=f"Failed to delete entry by ID: {str(e)}")

# endpoint to clear all history
@app.delete("/history/clear")
def clear_history():
    history.clear()
    save_history()
    return {"message": "All history cleared"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)