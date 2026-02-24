# app/api/v1/routers/memory.py
from fastapi import APIRouter, HTTPException, status, Depends, Query
import logging
from typing import List, Optional
from app.models.memory import MemoryCreate, MemoryUpdate, MemoryResponse
from app.modules import memory_manager
from pathlib import Path
import aiofiles

from app.server.dependencies import get_api_key

router = APIRouter(prefix="/v1/memory", dependencies=[Depends(get_api_key)])

logger = logging.getLogger(__name__)


@router.get(
    "/search_memory_file/{filename}",
    response_model=MemoryResponse,
    operation_id="search_memory_file",
    tags=["Memory"],
)
async def search_memory_file_endpoint(
    filename: str, parent_directory: Optional[str] = Query(default=None)
):
    """
    Searches for and reads the content of a file within the base memory path or a specified parent directory.

    Args:
        filename (str): The name of the file to search for. The .md extension will be automatically appended if not present.
        parent_directory (Optional[str]): The directory to start searching from, relative to BASE_MEMORY_PATH.
                                          If not provided, it will search from BASE_MEMORY_PATH.

    Returns:
        MemoryResponse: The details of the found file, including its content.

    Raises:
        HTTPException: If the file is not found (404 Not Found) or an internal server error occurs.
    """
    try:
        file_path = await memory_manager.read_search_from_parent(
            filename, parent_directory
        )
        async with aiofiles.open(file_path, mode="r") as f:
            content = await f.read()

        # Determine the directory relative to BASE_MEMORY_PATH
        relative_dir = str(
            file_path.parent.relative_to(memory_manager.BASE_MEMORY_PATH)
        )

        return MemoryResponse(
            directory=relative_dir,
            filename=filename,
            content=content,
            path=str(file_path),
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error searching memory file: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get(
    "/list_dirs",
    response_model=List[str],
    operation_id="list_top_directories",
    tags=["Memory"],
)
async def list_directories():
    """
    Lists all top-level memory directories.

    Returns:
        List[str]: A list of directory names.
    """
    try:
        directories = await memory_manager.list_memory_directories()
        return directories
    except Exception as e:
        logger.error(f"Error listing memory directories: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get(
    "/list_recursive/{directory:path}",
    response_model=List[str],
    operation_id="list_memories_recursive",
    tags=["Memory"],
)
async def list_memories_recursive(directory: str, max_depth: Optional[int] = None):
    """
    Lists all memory filenames within a specified directory and its subdirectories up to a certain depth.

    Args:
        directory (str): The name of the directory to list memories from.
        max_depth (Optional[int]): The maximum depth to search for memories. None for infinite depth.

    Returns:
        List[str]: A list of memory filenames (without .md extension).

    Raises:
        HTTPException: If an internal server error occurs.
    """
    try:
        memories = await memory_manager.list_memories_recursive(directory, max_depth)
        return memories
    except Exception as e:
        logger.error(
            f"Error listing memories recursively in directory '{directory}': {e}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get(
    "/list/{directory:path}",
    response_model=List[str],
    operation_id="list_memories",
    tags=["Memory"],
)
async def list_memories(directory: str):
    """
    Lists all memory filenames within a specified directory.

    Args:
        directory (str): The name of the directory to list memories from.

    Returns:
        List[str]: A list of memory filenames (without .md extension).

    Raises:
        HTTPException: If an internal server error occurs.
    """
    try:
        memories = await memory_manager.list_memories_in_directory(directory)
        return memories
    except Exception as e:
        logger.error(f"Error listing memories in directory '{directory}': {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.post(
    "/crud/{directory:path}/{filename}",
    status_code=status.HTTP_201_CREATED,
    response_model=MemoryResponse,
    operation_id="create_memory",
    tags=["Memory"],
)
async def create_memory(directory: str, filename: str, memory: MemoryCreate):
    """
    Creates a new memory file with the given content in the specified directory.

    Args:
        directory (str): The directory where the memory file will be created.
        filename (str): The name of the memory file (without .md extension).
        memory (MemoryCreate): The request body containing the content for the new memory.

    Returns:
        MemoryResponse: The details of the created memory.

    Raises:
        HTTPException: If the file already exists (409 Conflict) or an internal server error occurs.
    """
    try:
        file_path = await memory_manager.create_memory_file(
            directory, filename, memory.content
        )
        return MemoryResponse(
            directory=directory,
            filename=filename,
            content=memory.content,
            path=str(file_path),
        )
    except FileExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating memory: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get(
    "/crud/{directory:path}/{filename}",
    response_model=MemoryResponse,
    operation_id="read_memory",
    tags=["Memory"],
)
async def read_memory(directory: str, filename: str):
    """
    Reads the content of a specific memory file.

    Args:
        directory (str): The directory where the memory file is located.
        filename (str): The name of the memory file (without .md extension).

    Returns:
        MemoryResponse: The details of the read memory, including its content.

    Raises:
        HTTPException: If the file is not found (404 Not Found) or an internal server error occurs.
    """
    try:
        content = await memory_manager.read_memory_file(directory, filename)
        file_path = memory_manager.BASE_MEMORY_PATH / directory / f"{filename}.md"
        return MemoryResponse(
            directory=directory, filename=filename, content=content, path=str(file_path)
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error reading memory: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.put(
    "/crud/{directory:path}/{filename}",
    response_model=MemoryResponse,
    operation_id="update_memory",
    tags=["Memory"],
)
async def update_memory(directory: str, filename: str, memory: MemoryUpdate):
    """
    Updates the content of an existing memory file.

    Args:
        directory (str): The directory where the memory file is located.
        filename (str): The name of the memory file (without .md extension).
        memory (MemoryUpdate): The request body containing the new content for the memory.

    Returns:
        MemoryResponse: The details of the updated memory.

    Raises:
        HTTPException: If the file is not found (404 Not Found) or an internal server error occurs.
    """
    try:
        file_path = await memory_manager.update_memory_file(
            directory, filename, memory.content
        )
        return MemoryResponse(
            directory=directory,
            filename=filename,
            content=memory.content,
            path=str(file_path),
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating memory: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.delete(
    "/crud/{directory:path}/{filename}",
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="delete_memory",
    tags=["Memory"],
)
async def delete_memory(directory: str, filename: str):
    """
    Deletes a specific memory file.

    Args:
        directory (str): The directory where the memory file is located.
        filename (str): The name of the memory file (without .md extension).

    Returns:
        dict: A success message upon successful deletion.

    Raises:
        HTTPException: If the file is not found (404 Not Found) or an internal server error occurs.
    """
    try:
        await memory_manager.delete_memory_file(directory, filename)
        return {"message": "Memory deleted successfully."}
    except FileNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error deleting memory: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
