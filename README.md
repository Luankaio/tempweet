# TempWeet API

Uma API simples para um sistema de tweets usando FastAPI e MongoDB.

## Recursos

- **Usuários**: CRUD completo para gerenciamento de usuários
- **Tweets**: CRUD completo para tweets
- **Curtidas**: Sistema de curtidas/descurtidas
- **Comentários**: Sistema de comentários em tweets
- **Paginação**: Suporte a paginação nas listagens

## Instalação

1. Clone o repositório
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure o MongoDB (certifique-se que está rodando na porta padrão 27017)

4. Execute a aplicação:
```bash
python run.py
```

A API estará disponível em `http://localhost:8000`

## Documentação da API

Acesse `http://localhost:8000/docs` para ver a documentação interativa do Swagger.

## Endpoints Principais

### Usuários
- `POST /users/` - Criar usuário
- `GET /users/` - Listar usuários
- `GET /users/{user_id}` - Buscar usuário por ID
- `DELETE /users/{user_id}` - Deletar usuário

### Tweets
- `POST /tweets/` - Criar tweet
- `GET /tweets/` - Listar tweets (com paginação)
- `GET /tweets/{tweet_id}` - Buscar tweet por ID
- `PUT /tweets/{tweet_id}` - Atualizar tweet
- `DELETE /tweets/{tweet_id}` - Deletar tweet
- `POST /tweets/{tweet_id}/like` - Curtir/descurtir tweet
- `POST /tweets/{tweet_id}/comments` - Adicionar comentário
- `GET /tweets/user/{user_id}` - Buscar tweets de um usuário

## Estrutura dos Dados

### User
```json
{
  "username": "string",
  "email": "string"
}
```

### Tweet
```json
{
  "user_id": "string",
  "content": "string"
}
```

### Comment
```json
{
  "user_id": "string",
  "content": "string"
}
```

## Exemplo de Uso

1. **Criar um usuário:**
```bash
curl -X POST "http://localhost:8000/users/" \
     -H "Content-Type: application/json" \
     -d '{"username": "joao", "email": "joao@email.com"}'
```

2. **Criar um tweet:**
```bash
curl -X POST "http://localhost:8000/tweets/" \
     -H "Content-Type: application/json" \
     -d '{"user_id": "USER_ID_AQUI", "content": "Meu primeiro tweet!"}'
```

3. **Curtir um tweet:**
```bash
curl -X POST "http://localhost:8000/tweets/TWEET_ID/like?user_id=USER_ID"
```

## Estrutura do Projeto

```
tempweet/
├── app/
│   ├── __init__.py
│   ├── main.py          # Aplicação principal
│   ├── models.py        # Modelos Pydantic
│   ├── database.py      # Configuração do MongoDB
│   └── routes/
│       ├── __init__.py
│       ├── users.py     # Rotas de usuários
│       └── tweets.py    # Rotas de tweets
├── requirements.txt
├── run.py              # Script para executar a aplicação
├── .env               # Variáveis de ambiente
└── README.md
```
