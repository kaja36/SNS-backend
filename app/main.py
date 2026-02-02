from fastapi import FastAPI
import uvicorn
from api import api_router
from schemas import *
from db.database import Database

# dbクラスを生成
db = Database("sns.db")
# dbを初期化
db.init_db()

app = FastAPI()

app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
