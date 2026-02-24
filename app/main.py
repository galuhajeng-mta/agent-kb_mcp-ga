from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
from dotenv import load_dotenv

from app.server.logging import LoggingMiddleware
from app.api.v1.routers.memory import router as memory_v1_router
from app.api.v1.routers.ticket import router as ticket_router
from app.api.v2.routers.tools import router as tools_v2_router
# from app.db import init_db

# Load ENV sekali di awal
load_dotenv()

app = FastAPI(
    title="Central Memory API and MCP Server",
    description="API for Memory Management of LLMs and Users Alike.",
)

# Middleware
app.add_middleware(LoggingMiddleware)

# # 🔑 INIT DB SAAT APP START
# @app.on_event("startup")
# def on_startup():
#     init_db()

# ================= ROUTERS =================

app.include_router(
    memory_v1_router,
    prefix="/api/v1/memory",
    tags=["v1 - Memory Tools"],
)

app.include_router(
    ticket_router,
    prefix="/api/v1",
    tags=["v1 - Ticket"],
)

app.include_router(
    tools_v2_router,
    prefix="/api/v2/tools",
    tags=["v2 - Skill Provider"],
)

# ================= ROOT =================

@app.get("/")
def read_root():
    return {"message": "Service is running!"}

# ================= MCP =================

mcp = FastApiMCP(app)
mcp.mount_http()
mcp.mount_sse()
