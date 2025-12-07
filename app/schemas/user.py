from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    id: int
    username: Optional[str] = Field(default=None, max_length=50)


class UserResponse(BaseModel):
    id: int
    username: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

