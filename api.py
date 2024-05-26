from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sklearn.feature_extraction.text import TfidfVectorizer
import torch
from pydantic import BaseModel
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import torch.nn as nn
import torch.nn.functional as F
import pickle

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST","PUT"],
    allow_headers=["*"],
)

class ClassifierNN(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(ClassifierNN, self).__init__()
        self.n1 = nn.Linear(input_size, hidden_size)
        self.n2 = nn.Linear(hidden_size, hidden_size)
        self.n3 = nn.Linear(hidden_size, 1)

    def forward(self, x):
        x = F.relu(self.n1(x))
        x = F.relu(self.n2(x))
        x = self.n3(x)
        return x

model_path = "model_weights.pth"
tfidf_path = "tfidf_vectorizer.pkl"

try:
    with open(tfidf_path, "rb") as f:
        tfidf_vectorizer: TfidfVectorizer = pickle.load(f)
    
    input_size = len(tfidf_vectorizer.get_feature_names_out())
    model = ClassifierNN((input_size), 8)  
    model.load_state_dict(torch.load(model_path))
    model.eval()
    
except FileNotFoundError:
    print("Error: Model file not found!")
    
except Exception as e:
    print(f"Error loading model: {e}")


class InputData(BaseModel):
    title: str
    text: str

stop_words = set(stopwords.words("english"))



def preprocess_text(text):
    
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text) 
    text = re.sub(r"\s+", " ", text)  
    text_tokens = word_tokenize(text)
    text_tokens = [word for word in text_tokens if word not in stop_words]
    return " ".join(text_tokens)

@app.post("/predict")
async def predict(data: InputData):
    
    title = preprocess_text(data.title)
    text = preprocess_text(data.text)

    features = tfidf_vectorizer.transform([title + " " + text])
    features_tensor = torch.from_numpy(features.toarray()).float()

    with torch.no_grad():
        outputs = model(features_tensor)
        if torch.isnan(outputs).any() or torch.isinf(outputs).any():
            return {"error": "Invalid model output!"}
        
        predicted = torch.round(torch.sigmoid(outputs))
    
    return {"predicted_class": predicted.item()}
