from fastapi import APIRouter

router = APIRouter()

@router.get("/mcp")
def mcp_info():
    return {
        "name": "kb_mcp",
        "version": "0.1.0",
        "description": "Knowledge Base MCP",
        "tools": [
            {
                "name": "search_kb",
                "description": "Search knowledge base",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"}
                    },
                    "required": ["query"]
                }
            }
        ]
    }

@router.post("/mcp/invoke")
def invoke(payload: dict):
    query = payload.get("args", {}).get("query", "")
    return {
        "result": f"Hasil pencarian untuk: {query}"
    }
