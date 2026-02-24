from cryptography.fernet import Fernet
import json
import os

key = os.environ["FERNET_SECRET_KEY"]
f = Fernet(key.encode())

payload = {
    "staff_id": 101,
    "role": "supervisor"
}

token = f.encrypt(json.dumps(payload).encode()).decode()
print(token)