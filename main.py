from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import re
from scipy.sparse import hstack


model = joblib.load("spam_model.joblib")
vectorizer = joblib.load("tfidf_vectorizer.joblib")
scaler = joblib.load("scaler.joblib")

app = FastAPI()


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

# pydantic model for input data validation
class EmailInput(BaseModel):
    text: str
    
# API endpoint for spam prediction
@app.post("/predict/")
def predict_spam(data: EmailInput):
    text = data.text
    clean = clean_text(text)
    char_len = len(clean)
    word_len = len(clean.split())
    special_char_count = count_special_chars(text)
    has_url = int("url" in clean.lower())

    text_tfidf = vectorizer.transform([clean])
    numeric_features = np.array([[char_len, word_len, special_char_count, has_url]])
    numeric_scaled = scaler.transform(numeric_features)

    features = hstack([text_tfidf, numeric_scaled])

    prediction = model.predict(features)[0]
    probs = model.predict_proba(features)[0]
    label = "spam" if prediction == 1 else "ham"
    confidence = float(probs[prediction])
    return {"prediction": label
            , "confidence":round(confidence, 2)}
