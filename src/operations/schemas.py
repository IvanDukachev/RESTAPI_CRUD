from typing import Optional
from pydantic import BaseModel


class OperationCreate(BaseModel):
    name: str
    description: str

class OperationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
