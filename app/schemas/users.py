from pydantic import BaseModel
from datetime import datetime

# ==================== Request ====================
class Signup(BaseModel):
    username: str
    password: str

class Login(BaseModel):
    username: str
    password: str

class UpdateUser(BaseModel):
    username: str
    biography: str
    avatar_img: str

class UpdatePassword(BaseModel):
    password: str

# ==================== Response ====================
class ResponseToken(BaseModel):
    # access_token: str
    username: str

class ResponseUser(BaseModel):
    username: str
    biography: str
    avatar_img: str
    created_at: datetime

# ==================== OTHER ====================
import sqlite3

# sqlite3のRowをResponseUserに変換する関数
def row_to_response_user(row: sqlite3.Row) -> ResponseUser:
    return ResponseUser(
        username=row["username"],
        biography=row["biography"],
        avatar_img=row["avatar_img"],
        created_at=row["created_at"],
    )
