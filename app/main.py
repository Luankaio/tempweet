from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import connect_to_mongo, close_mongo_connection
from app.routes import users, tweets

app = FastAPI(
    title="TempWeet API",
    description="Uma API simples para um sistema de tweets",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Eventos de inicialização e finalização
@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

# Incluir rotas
app.include_router(users.router)
app.include_router(tweets.router)

@app.get("/")
async def root():
    return {"message": "Bem-vindo ao TempWeet API!"}