import yaml
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any

from app.skills.implementations import AVAILABLE_SKILLS
from app.server.dependencies import get_api_key

router = APIRouter()

# --- Skema Pydantic untuk Validasi ---

class ToolExecutionRequest(BaseModel):
    tool_name: str = Field(..., description="Nama skill yang akan dieksekusi.")
    arguments: Dict[str, Any] = Field(..., description="Argumen untuk skill dalam bentuk dictionary.")

# --- Endpoints ---

@router.get("/definitions")
def get_tool_definitions(api_key: str = Depends(get_api_key)):
    """
    Mengembalikan daftar semua 'skills' (tools) yang tersedia 
    dalam format JSON, diambil dari file definitions.yaml.
    Ini memungkinkan sistem eksternal (LLM agnostic Anda) untuk mengetahui
    alat apa saja yang bisa digunakan.
    """
    try:
        with open("app/skills/definitions.yaml", "r") as f:
            definitions = yaml.safe_load(f)
        return definitions.get("tools", [])
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File definisi skills tidak ditemukan.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal membaca definisi: {e}")

@router.post("/execute", summary="Execute internal tool", operation_id="execute_tool")
async def execute_tool(
    request: ToolExecutionRequest,
    api_key: str = Depends(get_api_key)
):
    """
    Mengeksekusi sebuah 'skill' (tool) dengan nama dan argumen yang diberikan.
    Sistem LLM agnostik Anda akan memanggil endpoint ini setelah memutuskan
    tool mana yang akan digunakan.
    """
    tool_name = request.tool_name
    arguments = request.arguments

    if tool_name not in AVAILABLE_SKILLS:
        raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' tidak ditemukan.")

    try:
        tool_function = AVAILABLE_SKILLS[tool_name]
        # Menggunakan ** untuk 'unpack' dictionary argumen menjadi keyword arguments fungsi
        result = await tool_function(**arguments)
        return {"result": result}
    except TypeError as e:
        # Error ini biasanya terjadi jika argumen yang diberikan tidak cocok dengan signature fungsi
        raise HTTPException(status_code=400, detail=f"Argumen tidak valid untuk tool '{tool_name}': {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Terjadi error saat eksekusi tool '{tool_name}': {e}")