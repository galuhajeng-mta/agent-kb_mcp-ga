import json
import os
from fastapi import Header, HTTPException
from cryptography.fernet import Fernet

def get_current_auth(authorization: str = Header(...)):
    try:
        if not authorization.startswith("Bearer "):
            raise Exception("invalid header")

        token = authorization.replace("Bearer ", "").encode()
        key = os.environ["FERNET_SECRET_KEY"].encode()

        fernet = Fernet(key)
        decrypted = fernet.decrypt(token)

        auth_data = json.loads(decrypted.decode())
        return auth_data

    except Exception:
        raise HTTPException(status_code=403, detail="invalid authorization")