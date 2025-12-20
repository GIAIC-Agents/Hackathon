import requests
import json
import sys

url = "http://localhost:8000/api/rag/query"
payload = {"query": "What is this book about?"}
headers = {"Content-Type": "application/json"}

print(f"Testing URL: {url}")
try:
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}") # Print raw text in case JSON conversion fails
except Exception as e:
    print(f"Error: {e}")
