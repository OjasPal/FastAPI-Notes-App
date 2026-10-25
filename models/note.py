from datetime import datetime, timezone

from pydantic import BaseModel, Field


class Note(BaseModel):
    title: str
    desc: str
    important: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))