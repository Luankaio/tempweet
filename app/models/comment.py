from typing import Optional
from uuid import uuid4
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class Comment(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    comment_id: str = None
    user_id: str
    content: str
    created_at: datetime = None
    updated_at: datetime = None
    is_active: Optional[bool] = True
    
    def __init__(self, **data):
        if 'comment_id' not in data or data['comment_id'] is None:
            data['comment_id'] = str(uuid4())
        if 'created_at' not in data or data['created_at'] is None:
            data['created_at'] = datetime.utcnow()
        if 'updated_at' not in data or data['updated_at'] is None:
            data['updated_at'] = datetime.utcnow()
        super().__init__(**data)
    
    def serialize(self):
        return self.model_dump()

class CommentCreate(BaseModel):
    user_id: str
    content: str
