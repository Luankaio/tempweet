from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models import User, UserCreate, UserUpdate
from app.database import get_database

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=dict)
async def create_user(user_data: UserCreate, db=Depends(get_database)):
    """Criar um novo usuário"""
    user_dict = user_data.model_dump()
    
    # Verificar se username já existe
    existing_user = await db.users.find_one({"username": user_dict["username"]})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username já existe")
    
    # Verificar se email já existe
    existing_email = await db.users.find_one({"email": user_dict["email"]})
    if existing_email:
        raise HTTPException(status_code=400, detail="Email já existe")
    
    # Criar o usuário usando o modelo
    user = User(**user_dict)
    user_dict = user.model_dump()
    
    await db.users.insert_one(user_dict)
    return user.serialize()

@router.get("/", response_model=List[dict])
async def get_users(db=Depends(get_database)):
    """Listar todos os usuários"""
    users = []
    async for user_data in db.users.find():
        user = User(**user_data)
        users.append(user.serialize())
    return users

@router.get("/{user_id}", response_model=dict)
async def get_user(user_id: str, db=Depends(get_database)):
    """Buscar usuário por ID"""
    user_data = await db.users.find_one({"user_id": user_id})
    if not user_data:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    user = User(**user_data)
    return user.serialize()

@router.delete("/{user_id}")
async def delete_user(user_id: str, db=Depends(get_database)):
    """Deletar usuário"""
    result = await db.users.delete_one({"user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return {"message": "Usuário deletado com sucesso"}
