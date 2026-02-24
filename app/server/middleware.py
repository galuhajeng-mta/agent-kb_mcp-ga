# app/server/middleware.py

from starlette.requests import Request
from starlette.responses import JSONResponse

API_KEYS = ["super-secret-key-1", "another-super-secret-key-2"]


# ! Not implemented yet
async def api_key_middleware(request: Request, call_next):
    # This middleware will check for the API key on every request.
    # You can add logic here to explicitly exclude certain paths if needed.
    # For example: if request.url.path.startswith("/docs"): ...

    api_key = request.headers.get("X-API-Key")

    if not api_key or api_key not in API_KEYS:
        return JSONResponse(
            status_code=403, content={"detail": "Invalid or missing API key"}
        )

    # If the API key is valid, proceed to the next middleware or endpoint.
    response = await call_next(request)
    return response
