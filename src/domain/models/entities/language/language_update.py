from pydantic import BaseModel, Field, UUID4
from typing import Optional
from datetime import datetime

class LanguageUpdate(BaseModel):
    id: UUID4 = Field(...)
    name: str = Field(..., max_length=100)
    code: str = Field(..., max_length=10)
    native_name: Optional[str] = Field(default=None, max_length=100)
    state: bool = Field(default=True)
