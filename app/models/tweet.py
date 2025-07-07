from typing import Optional, List
from uuid import uuid4
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from .comment import Comment

class Tweet(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    tweet_id: str = None
    user_id: str
    content: str
    likes: List[str] = []  # Lista de user_ids que curtiram
    comments: List[Comment] = []
    created_at: datetime = None
    updated_at: datetime = None
    is_active: Optional[bool] = True
    
    def __init__(self, **data):
        if 'tweet_id' not in data or data['tweet_id'] is None:
            data['tweet_id'] = str(uuid4())
        if 'created_at' not in data or data['created_at'] is None:
            data['created_at'] = datetime.utcnow()
        if 'updated_at' not in data or data['updated_at'] is None:
            data['updated_at'] = datetime.utcnow()
        if 'likes' not in data:
            data['likes'] = []
        if 'comments' not in data:
            data['comments'] = []
        super().__init__(**data)
    
    def serialize(self):
        return self.model_dump()

class TweetCreate(BaseModel):
    user_id: str
    content: str

class TweetUpdate(BaseModel):
    content: Optional[str] = None
