# Central Memory: A Skill Provider for LLM Systems

## Problem

Prompts, instructions, and AI-related memory were scattered everywhere. Notebooks, random documents, code comments—our knowledge base was fragmented. Reusing or evaluating prompts was a hunt. This inconsistency created a chaotic development cycle where a shared knowledge base should have existed.

## Solution: A Dual API Architecture

The Central Memory App was created to bring order to this chaos. It serves as a centralized, versioned repository for AI-related knowledge, built on FastAPI.

With its latest evolution, the application now operates on a **dual API architecture**, making it both a direct memory store and a powerful, LLM-agnostic **Skill Provider**.

*   **API v1 (Direct Memory Access)**: A stable, imperative API for direct CRUD operations on memory files. It acts as a reliable "data warehouse."
*   **API v2 (Skill Provider)**: A declarative, more abstract API that exposes the system's capabilities as "skills" or "tools." This allows any external LLM or AI agent to query what the service can *do* and then command it to execute those skills.

This dual approach ensures backward compatibility while paving the way for more intelligent, agent-based systems.

## Key Features

*   **Dual API Architecture**: Supports both direct file access (v1) and skill-based execution (v2).
*   **LLM Agnostic**: Designed to be a tool provider for any external LLM system (e.g., LangChain, custom agents).
*   **Skill Definition**: Exposes its capabilities through a `/definitions` endpoint, allowing dynamic tool discovery.
*   **Hierarchical Storage**: Uses human-readable Markdown files in a clear directory structure.
*   **Dockerized**: Fully containerized with Docker Compose for consistent and easy deployment.

## Architecture in Story

Think of the Central Memory App as a **specialized workshop**.

*   **The Data (`central-memory-data/`)**: This is the workshop's raw material inventory—piles of wood, metal, and schematics (your Markdown files).
*   **API v1**: This is like having a key to the inventory room. You can go in, grab exactly what you need (`read_memory`), and take it back to your own workshop to process. You do all the work.
*   **API v2**: This is like talking to the workshop's **master craftsperson**. You don't ask for raw materials. Instead, you ask, *"What can you build?"* (`GET /api/v2/tools/definitions`). The craftsperson shows you a catalog of finished products (skills like `search_memory_by_keyword`). You then say, *"Build me that one, using these schematics."* (`POST /api/v2/tools/execute`). The craftsperson does the work and gives you the finished product.

## Development Setup

### Prerequisites
- Python 3.11 or higher
- Docker and Docker Compose

### Local Development
1.  **Clone the repository**:
    ```bash
    git clone https://github.com/mta-tech/central-memory.git
    cd central-memory
    ```
2.  **Initialize Python environment with `uv`**:
    ```bash
    uv venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```
3.  **Install dependencies**:
    ```bash
    uv sync
    ```
4.  **Create environment file**:
    Copy `.env.example` to `.env`. The only key you need for this service is `API_KEY`.
    ```bash
    cp .env.example .env
    ```
    **File: `.env`**
    ```env
    # A secret key to protect your API endpoints.
    API_KEY="YOUR_SUPER_SECRET_KEY"
    ```
5.  **Run the application**:
    ```bash
    python -m uvicorn app.main:app --host 0.0.0.0 --port 7310 --reload
    ```
    The application will be accessible at `http://localhost:7310`.

## API Endpoints

The service exposes two versions of the API.

### API v1: Direct Memory Access

These endpoints are for direct, low-level access to memory files.

*   `GET /api/v1/memory/list_directories`: Lists all top-level directories.
*   `GET /api/v1/memory/list_memories`: Lists all memories in a directory.
*   `POST /api/v1/memory/read_memory`: Reads the content of a specific memory file.
*   *(Other CRUD endpoints...)*

### API v2: Skill Provider

These endpoints allow an external system to discover and execute skills.

#### 1. Get Skill Definitions

Ask the service what tools it has available.

*   **Endpoint**: `GET /api/v2/tools/definitions`
*   **`curl` Example**:
    ```bash
    curl -X GET http://localhost:7310/api/v2/tools/definitions \
    -H "Authorization: YOUR_SUPER_SECRET_KEY"
    ```
*   **Expected Response**: A JSON array describing the available skills, their purpose, and required arguments.

#### 2. Execute a Skill

Command the service to execute a specific skill with given arguments.

*   **Endpoint**: `POST /api/v2/tools/execute`
*   **`curl` Example (Windows CMD)**:
    ```bash
    curl -X POST http://localhost:7310/api/v2/tools/execute ^
    -H "Content-Type: application/json" ^
    -H "Authorization: YOUR_SUPER_SECRET_KEY" ^
    -d "{
      \"tool_name\": \"search_memory_by_keyword\",
      \"arguments\": {
        \"directory_name\": \"\",
        \"file_name\": \"restaurant_menu.md\",
        \"keyword\": \"Salad\"
      }
    }"
    ```
*   **Expected Response**: A JSON object containing the result of the skill's execution.

## How to Add a New Skill

1.  **Define the Skill**: Add a new entry to `app/skills/definitions.yaml`. Describe what the skill does and what inputs (`input_schema`) it needs.
2.  **Implement the Logic**: Write the corresponding Python function in `app/skills/implementations.py`. The function name must match the `name` in the YAML definition.
3.  **Register the Function**: Add the new function to the `AVAILABLE_SKILLS` dictionary at the bottom of `app/skills/implementations.py`.

The service will automatically detect and expose the new skill through the API v2 endpoints.

## Contributing
Contributions are welcome! Please refer to the project's guidelines for more information.
