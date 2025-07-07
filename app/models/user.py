from typing import Optional
from uuid import uuid4
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime

class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    user_id: str = None
    username: str
    email: EmailStr
    password: str
    created_at: datetime = None
    updated_at: datetime = None
    is_active: Optional[bool] = True
    role: str = "user"
    
    def __init__(self, **data):
        if 'user_id' not in data or data['user_id'] is None:
            data['user_id'] = str(uuid4())
        if 'created_at' not in data or data['created_at'] is None:
            data['created_at'] = datetime.utcnow()
        if 'updated_at' not in data or data['updated_at'] is None:
            data['updated_at'] = datetime.utcnow()
        super().__init__(**data)
    
    def serialize(self):
        return self.model_dump(exclude={'password'})

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Optional[str] = "user"

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[str] = None
