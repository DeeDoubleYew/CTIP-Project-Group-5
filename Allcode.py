import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from scipy.sparse import hstack, csr_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS  ## WordCloud throws error without this
from pathlib import Path
import secrets

file_path = Path("assets") / "datasets" / "emails.csv" 
df = pd.read_csv(file_path)
print("Shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nNulls per column:\n", df.isna().sum())
print("\nDtypes:\n", df.dtypes)
duplicate = df.duplicated(subset=["text"]).sum()
print(f"\nNumber of rows with duplicates: {duplicate}")
print("\n ")

print("\nClass balance (0=ham, 1=spam):")
print(df["spam"].value_counts())
print("Spam rate:", round(df["spam"].mean(), 3))
before = len(df)
df = df.drop_duplicates(subset=["text"]).reset_index(drop=True)

df["text"] = df["text"].astype(str).str.replace(r"\s+", " ", regex=True).str.strip()
print(f"Dropped {before - len(df)} duplicates. New total:", len(df))



URL_PATTERN = re.compile(r"http[s]?://\S+|www\.\S+") 
EMAIL_PATTERN = re.compile(r"\b[\w\.-]+@[\w\.-]+\.\w+\b") 
PHONE_PATTERN = re.compile(r'\b\d{3}-\d{3}-\d{4}\b') 
MONEY_PATTERN = re.compile(r'\$+\s*\d[\d\s,]*(?:[.]\d+)?') 


def clean_text(s: str) -> str:
    s = str(s).lower()
    s = re.sub(r"^subject:\s*", "", s) #remove "subject:" at the start of the text
    s = re.sub(r'\s*([^\w\s])\s*', r'\1', s) #remove the extra one space around punctuation.
    s = URL_PATTERN.sub(" URL ", s) #replace any links with the literal word URL 
    s = PHONE_PATTERN.sub(" PHONENUMBER ", s) #replace phone numbers with PHONENUMBER
    s = EMAIL_PATTERN.sub(" EMAIL ", s) #replace emails with EMAIL 
    s = MONEY_PATTERN.sub(" MONEY ", s) #replace numeric money into MONEY 
    s = re.sub(r'@\w+', '', s) #delete any mentions
    s = re.sub(r"[^a-zA-Z0-9\s]", " ", s) #remove special characters
    s = re.sub(r'\s+', ' ', s).strip()  # fix spaces and trim the end
    return s  

def count_special_chars(text):
    return len(re.findall(r'[!$%&*@#_?]', str(text))) 


df["text_clean"] = df["text"].apply(clean_text)
df = df.drop_duplicates(subset=["text_clean"]).reset_index(drop=True)

df["char_len"] = df["text_clean"].str.len()
df["word_len"] = df["text_clean"].str.split().str.len()
df["special_char_count"] = df["text"].apply(count_special_chars)
df["has_url"]  = df["text_clean"].str.contains(r"\bURL\b").astype(int)

print("Rows after cleaning:", len(df))

X = df[["text_clean", "char_len", "word_len","special_char_count", "has_url"]]
y = df["spam"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)
q1 = X_train["char_len"].quantile(0.25)
q3 = X_train["char_len"].quantile(0.75)
iqr = q3 - q1
upper = q3 + 1.5 * iqr

X_train = X_train[X_train["char_len"] <= upper]
y_train = y_train.loc[X_train.index]


vectorizer = TfidfVectorizer(ngram_range=(1,1), max_features=5000,  stop_words="english")
X_train_tfidf = vectorizer.fit_transform(X_train["text_clean"])
X_test_tfidf  = vectorizer.transform(X_test["text_clean"])



numeric_cols = ["char_len", "word_len", "special_char_count", "has_url"]
numeric_train = X_train[numeric_cols]
numeric_test  = X_test[numeric_cols]

scaler = StandardScaler()
numeric_train_scaled = scaler.fit_transform(numeric_train)
numeric_test_scaled  = scaler.transform(numeric_test)

# Combine TF-IDF and numeric arrays
X_train_final = hstack([X_train_tfidf, numeric_train_scaled])
X_test_final  = hstack([X_test_tfidf, numeric_test_scaled])

X_train_final_array = X_train_final.toarray()

logreg = LogisticRegression(C=0.3, class_weight={0:1, 1:4}, max_iter=1000, random_state=42)
logreg.fit(X_train_final_array, y_train)


y_pred = logreg.predict(X_train_final_array)
acc  = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred)
rec  = recall_score(y_test, y_pred)
f1   = f1_score(y_test, y_pred)
cm   = confusion_matrix(y_test, y_pred)

print("\n=== Logistic Regression Results ===")
print(f"Accuracy : {acc:.4f}")
print(f"Precision: {prec:.4f}")
print(f"Recall   : {rec:.4f}")
print(f"F1 Score : {f1:.4f}")
print("Confusion Matrix:\n", cm)

import joblib
joblib.dump(logreg, "spam_model.joblib")
joblib.dump(vectorizer, "tfidf_vectorizer.joblib")
joblib.dump(scaler, "scaler.joblib")


