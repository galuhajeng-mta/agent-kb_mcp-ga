from dotenv import load_dotenv
import os

load_dotenv()

def get_env(key: str, required: bool = True) -> str | None:
    value = os.getenv(key)

    if required and not value:
        raise RuntimeError(f"Missing required environment variable: {key}")

    return value


# MCP
API_KEY= get_env("API_KEY")

if __name__ == "__main__":
    print("API_KEY:", API_KEY)
