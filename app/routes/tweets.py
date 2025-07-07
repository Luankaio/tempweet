from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import datetime
from app.models import Tweet, TweetCreate, TweetUpdate, Comment, CommentCreate
from app.database import get_database

router = APIRouter(prefix="/tweets", tags=["tweets"])

@router.post("/", response_model=dict)
async def create_tweet(tweet_data: TweetCreate, db=Depends(get_database)):
    """Criar um novo tweet"""
    # Verificar se o usuário existe
    user = await db.users.find_one({"user_id": tweet_data.user_id})
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Criar o tweet usando o modelo
    tweet = Tweet(**tweet_data.model_dump())
    tweet_dict = tweet.model_dump()
    
    await db.tweets.insert_one(tweet_dict)
    return tweet.serialize()

@router.get("/", response_model=List[dict])
async def get_tweets(skip: int = 0, limit: int = 20, db=Depends(get_database)):
    """Listar tweets com paginação"""
    tweets = []
    async for tweet_data in db.tweets.find().sort("created_at", -1).skip(skip).limit(limit):
        tweet = Tweet(**tweet_data)
        tweets.append(tweet.serialize())
    return tweets

@router.get("/{tweet_id}", response_model=dict)
async def get_tweet(tweet_id: str, db=Depends(get_database)):
    """Buscar tweet por ID"""
    tweet_data = await db.tweets.find_one({"tweet_id": tweet_id})
    if not tweet_data:
        raise HTTPException(status_code=404, detail="Tweet não encontrado")
    
    tweet = Tweet(**tweet_data)
    return tweet.serialize()

@router.put("/{tweet_id}", response_model=dict)
async def update_tweet(tweet_id: str, tweet_update: TweetUpdate, db=Depends(get_database)):
    """Atualizar tweet"""
    update_data = {k: v for k, v in tweet_update.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
    
    update_data["updated_at"] = datetime.utcnow()
    
    result = await db.tweets.update_one(
        {"tweet_id": tweet_id}, 
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Tweet não encontrado")
    
    tweet_data = await db.tweets.find_one({"tweet_id": tweet_id})
    tweet = Tweet(**tweet_data)
    return tweet.serialize()

@router.delete("/{tweet_id}")
async def delete_tweet(tweet_id: str, db=Depends(get_database)):
    """Deletar tweet"""
    result = await db.tweets.delete_one({"tweet_id": tweet_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Tweet não encontrado")
    
    return {"message": "Tweet deletado com sucesso"}

@router.post("/{tweet_id}/like")
async def like_tweet(tweet_id: str, user_id: str, db=Depends(get_database)):
    """Curtir ou descurtir um tweet"""
    # Verificar se o usuário existe
    user = await db.users.find_one({"user_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    tweet_data = await db.tweets.find_one({"tweet_id": tweet_id})
    if not tweet_data:
        raise HTTPException(status_code=404, detail="Tweet não encontrado")
    
    likes = tweet_data.get("likes", [])
    
    if user_id in likes:
        # Remover curtida
        await db.tweets.update_one(
            {"tweet_id": tweet_id},
            {"$pull": {"likes": user_id}}
        )
        message = "Curtida removida"
    else:
        # Adicionar curtida
        await db.tweets.update_one(
            {"tweet_id": tweet_id},
            {"$push": {"likes": user_id}}
        )
        message = "Tweet curtido"
    
    return {"message": message}

@router.post("/{tweet_id}/comments", response_model=dict)
async def add_comment(tweet_id: str, comment_data: CommentCreate, db=Depends(get_database)):
    """Adicionar comentário a um tweet"""
    # Verificar se o usuário existe
    user = await db.users.find_one({"user_id": comment_data.user_id})
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    tweet_data = await db.tweets.find_one({"tweet_id": tweet_id})
    if not tweet_data:
        raise HTTPException(status_code=404, detail="Tweet não encontrado")
    
    # Criar o comentário usando o modelo
    comment = Comment(**comment_data.model_dump())
    comment_dict = comment.model_dump()
    
    await db.tweets.update_one(
        {"tweet_id": tweet_id},
        {"$push": {"comments": comment_dict}}
    )
    
    updated_tweet_data = await db.tweets.find_one({"tweet_id": tweet_id})
    updated_tweet = Tweet(**updated_tweet_data)
    return updated_tweet.serialize()

@router.get("/user/{user_id}", response_model=List[dict])
async def get_user_tweets(user_id: str, skip: int = 0, limit: int = 20, db=Depends(get_database)):
    """Buscar tweets de um usuário específico"""
    tweets = []
    async for tweet_data in db.tweets.find({"user_id": user_id}).sort("created_at", -1).skip(skip).limit(limit):
        tweet = Tweet(**tweet_data)
        tweets.append(tweet.serialize())
    return tweets
