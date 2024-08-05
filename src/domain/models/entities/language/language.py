from pydantic import BaseModel, Field, UUID4
from typing import Optional
from datetime import datetime

class language(BaseModel):
    id: Optional[UUID4] = Field(default=None)
    name: str = Field(..., max_length=100)
    code: str = Field(..., max_length=10)
    native_name: Optional[str] = Field(default=None, max_length=100)
    state: bool = Field(default=True)
    created_date: Optional[datetime] = Field(default_factory=datetime.now)
    updated_date: Optional[datetime] = Field(default_factory=datetime.now)

    def dict(self, *args, **kwargs):
        exclude = kwargs.pop("exclude", set())
        exclude.update({"created_date", "updated_date"})
        return super().model_dump(*args, exclude=exclude, **kwargs)
