from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    message: str
    user_ip: Optional[str] = None
    threadId: Optional[str] = None