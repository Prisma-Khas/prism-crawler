
import requests
import json

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL = "qwen3.8:27b"

payload = {
    "model": MODEL,
    "messages": [
        {
            "role": "user",
            "content": """
            Identify whether this is a social media post.

            Text:
            "Kerajaan perlu meningkatkan bantuan kepada rakyat."

            Return JSON:
            {
                "is_post": true,
                "language": "ms",
                "sentiment": "positive",
                "confidence": 0.95
            }
            """
        }
    ],
    "format": "json",
    "stream": False
}

response = requests.post(
    OLLAMA_URL,
    json=payload,
    timeout=300
)

response.raise_for_status()

result = response.json()

print(json.dumps(
    json.loads(result["message"]["content"]),
    indent=4,
    ensure_ascii=False
))
