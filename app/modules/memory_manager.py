import os
import aiofiles
from pathlib import Path
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

BASE_MEMORY_PATH = Path(os.getenv("CENTRAL_MEMORY_DATA_PATH", "central-memory-data"))


async def create_memory_file(directory: str, filename: str, content: str) -> Path:
    """Creates a new memory file."""
    dir_path = BASE_MEMORY_PATH / directory if directory else BASE_MEMORY_PATH
    file_path = dir_path / f"{filename}.md"

    if not dir_path.exists():
        dir_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {dir_path}")

    if file_path.exists():
        raise FileExistsError(
            f"Memory '{filename}' already exists in directory '{directory}'."
        )

    async with aiofiles.open(file_path, mode="w") as f:
        await f.write(content)
    logger.info(f"Created memory file: {file_path}")
    return file_path


async def read_memory_file(directory: str, filename: str) -> str:
    """Reads the content of a memory file."""
    dir_path = BASE_MEMORY_PATH / directory if directory else BASE_MEMORY_PATH
    file_path = dir_path / f"{filename}.md"
    if not file_path.exists():
        raise FileNotFoundError(
            f"Memory '{filename}' not found in directory '{directory}'."
        )

    async with aiofiles.open(file_path, mode="r") as f:
        content = await f.read()
    logger.info(f"Read memory file: {file_path}")
    return content


async def read_search_from_parent(
    filename: str, parent_directory: Optional[str] = None
) -> Path:
    """
    Reads the content of a file by searching from a specified parent directory within the base memory path.
    Returns the full path of the found file.
    """
    search_base_path = BASE_MEMORY_PATH
    if parent_directory:
        # Construct the full path for the parent_directory relative to BASE_MEMORY_PATH
        potential_search_path = BASE_MEMORY_PATH / parent_directory
        if potential_search_path.is_dir():
            search_base_path = potential_search_path
        else:
            logger.warning(
                f"Invalid or non-existent parent_directory '{parent_directory}' "
                f"relative to BASE_MEMORY_PATH. Searching from BASE_MEMORY_PATH instead."
            )

    # Append .md extension if not already present
    if not filename.endswith(".md"):
        filename_with_ext = f"{filename}.md"
    else:
        filename_with_ext = filename

    for root, _, files in os.walk(search_base_path):
        if filename_with_ext in files:
            file_path = Path(root) / filename_with_ext
            logger.info(f"Found file '{filename_with_ext}' at: {file_path}")
            return file_path

    raise FileNotFoundError(f"File '{filename}' not found in specified directories.")


async def update_memory_file(directory: str, filename: str, content: str) -> Path:
    """Updates the content of an existing memory file."""
    dir_path = BASE_MEMORY_PATH / directory if directory else BASE_MEMORY_PATH
    file_path = dir_path / f"{filename}.md"
    if not file_path.exists():
        raise FileNotFoundError(
            f"Memory '{filename}' not found in directory '{directory}'."
        )

    async with aiofiles.open(file_path, mode="w") as f:
        await f.write(content)
    logger.info(f"Updated memory file: {file_path}")
    return file_path


async def delete_memory_file(directory: str, filename: str):
    """Deletes a memory file."""
    dir_path = BASE_MEMORY_PATH / directory if directory else BASE_MEMORY_PATH
    file_path = dir_path / f"{filename}.md"
    if not file_path.exists():
        raise FileNotFoundError(
            f"Memory '{filename}' not found in directory '{directory}'."
        )

    os.remove(file_path)
    logger.info(f"Deleted memory file: {file_path}")

    # Clean up directory if empty
    dir_path = BASE_MEMORY_PATH / directory
    if not any(dir_path.iterdir()):
        os.rmdir(dir_path)
        logger.info(f"Deleted empty directory: {dir_path}")


async def list_memories_in_directory(directory: str) -> List[str]:
    """Lists all memory filenames in a given directory."""
    dir_path = BASE_MEMORY_PATH / directory
    if not dir_path.exists() or not dir_path.is_dir():
        return []

    memories = []
    for item in os.listdir(dir_path):
        if item.endswith(".md") and os.path.isfile(dir_path / item):
            memories.append(item[:-3])  # Remove .md extension
    logger.info(f"Listed memories in directory '{directory}': {memories}")
    return memories


async def list_memory_directories() -> List[str]:
    """Lists all top-level memory directories."""
    if not BASE_MEMORY_PATH.exists():
        return []

    directories = []
    for item in os.listdir(BASE_MEMORY_PATH):
        item_path = BASE_MEMORY_PATH / item
        if item_path.is_dir():
            directories.append(item)
    logger.info(f"Listed memory directories: {directories}")
    return directories


async def list_memories_recursive(directory: str, max_depth: int = None) -> List[str]:
    """
    Lists all memory filenames within a specified directory and its subdirectories up to a certain depth.
    """
    base_dir_path = BASE_MEMORY_PATH / directory
    if not base_dir_path.exists() or not base_dir_path.is_dir():
        return []

    memories = []
    for root, dirs, files in os.walk(base_dir_path):
        # Calculate current depth relative to the base_dir_path
        current_depth = len(Path(root).relative_to(base_dir_path).parts)

        # os.walk includes the base directory itself, which has a relative depth of 0.
        # If max_depth is 0, we only want files directly in base_dir_path.
        # If max_depth is 1, we want files in base_dir_path and its immediate subdirectories.
        # So, we check if current_depth is greater than max_depth.
        if max_depth is not None and current_depth > max_depth:
            del dirs[:]  # Don't traverse deeper into subdirectories
            continue

        for file in files:
            if file.endswith(".md"):
                relative_path = Path(root) / file
                # Store the path relative to BASE_MEMORY_PATH, without the .md extension
                memories.append(str(relative_path.relative_to(BASE_MEMORY_PATH))[:-3])
    logger.info(
        f"Listed memories recursively in directory '{directory}' (max_depth={max_depth}): {memories}"
    )
    return memories
