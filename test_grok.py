import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://api.x.ai/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.getenv('XAI_API_KEY')}"
}

payload = {
    "messages": [
        {
            "role": "system",
            "content": "You are a test assistant."
        },
        {
            "role": "user",
            "content": "Testing. Just say hi and hello world and nothing else."
        }
    ],
    "model": "grok-4-latest",
    "stream": False,
    "temperature": 0
}

response = requests.post(url, headers=headers, json=payload)
print("Status Code:", response.status_code)
print("Response:")
print(json.dumps(response.json(), indent=2))
