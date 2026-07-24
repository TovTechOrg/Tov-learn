from google import genai

client = genai.Client(
    vertexai=True,
    project="eternal-insight-501811-v4",
    location="us-central1",
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="אמור שלום בעברית",
)

print(response.text)
