from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import users, tweets

app = FastAPI(
    title="TempWeet API",
    description="Uma API simples para um sistema de tweets",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(tweets.router)

@app.get("/")
async def root():
    return {"message": "Bem-vindo ao TempWeet API!"}