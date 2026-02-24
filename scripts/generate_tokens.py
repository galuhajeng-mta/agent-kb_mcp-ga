import json
import os
from cryptography.fernet import Fernet
from sqlalchemy import create_engine, text

# ===== CONFIG =====
DATABASE_URL = os.environ["DATABASE_URL"]
FERNET_SECRET_KEY = os.environ["FERNET_SECRET_KEY"]
OUTPUT_FILE = "scripts/tokens.json"

# ===== SETUP =====
fernet = Fernet(FERNET_SECRET_KEY.encode())
engine = create_engine(DATABASE_URL)

def main():
    tokens = {}

    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT id, role FROM staff ORDER BY id")
        )

        for row in result:
            staff_id = row.id
            role = row.role

            payload = {
                "staff_id": staff_id,
                "role": role
            }

            token = fernet.encrypt(
                json.dumps(payload).encode()
            ).decode()

            tokens[str(staff_id)] = {
                "staff_id": staff_id,
                "role": role,
                "token": token
            }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(tokens, f, indent=2)

    print(f"✅ generated {len(tokens)} tokens")
    print(f"📄 saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
