# app/server/dependencies.py
import time
from typing import Optional, Type, TypeVar

from fastapi import Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
from app.server.config import Settings


def get_settings() -> Settings:
    return Settings()


# api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)
api_key_header = APIKeyHeader(name="Authorization", auto_error=True)


async def get_api_key(
    settings: Settings = Depends(get_settings), api_key: str = Security(api_key_header)
):
    # This check ensures the API key is not None and matches the one from your config
    if settings.API_KEY is None:
        return api_key  # Allow access if no API key is set

    if api_key != settings.API_KEY:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Invalid or missing API Key"
        )
    return api_key
