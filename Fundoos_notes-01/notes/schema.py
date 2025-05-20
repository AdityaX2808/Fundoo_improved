from pydantic import BaseModel
from typing import List , Optional

class NoteBase(BaseModel):
    title: str
    content: str

class NoteCreate(NoteBase):
    pass 

class NoteResponse(NoteBase):
    id: int
    labels: List[str] = []

    class Config:
        from_attributes = True