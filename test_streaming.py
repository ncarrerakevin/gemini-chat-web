#!/usr/bin/env python3
"""Script para probar el streaming"""

import requests
import json
import time

url = "http://localhost:5001/send"
headers = {"Content-Type": "application/json"}
data = {
    "message": "Hola Sans",
    "session_id": "test_sans_" + str(int(time.time()))
}

print("Probando streaming...")
print("-" * 50)

try:
    response = requests.post(url, json=data, stream=True, timeout=30)

    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print("-" * 50)
    print("Respuesta en streaming:")

    for line in response.iter_lines():
        if line:
            decoded = line.decode('utf-8')
            print(f">> {decoded}")

except Exception as e:
    print(f"Error: {e}")
