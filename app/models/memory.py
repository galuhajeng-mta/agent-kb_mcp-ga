from pydantic import BaseModel, Field
from typing import Optional


class MemoryCreate(BaseModel):
    content: str = Field(
        ..., description="The content of the memory in markdown format."
    )


class MemoryUpdate(BaseModel):
    content: str = Field(
        ..., description="The updated content of the memory in markdown format."
    )


class MemoryResponse(BaseModel):
    directory: str = Field(..., description="The directory where the memory is stored.")
    filename: str = Field(..., description="The filename of the memory.")
    content: str = Field(
        ..., description="The content of the memory in markdown format."
    )
    path: str = Field(..., description="The full path to the memory file.")
