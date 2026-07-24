from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class TextInput(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"message": "שרת ניתוח סנטימנט ישראלי"}

@app.post("/analyze")
def analyze_sentiment(input: TextInput):
    # In a real app, you would use a model here.
    # For this exercise, we'll use a simple rule.
    if "מעולה" in input.text or "מצוין" in input.text:
        sentiment = "positive"
    elif "גרוע" in input.text or "אכזבה" in input.text:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    
    return {"original_text": input.text, "sentiment": sentiment}