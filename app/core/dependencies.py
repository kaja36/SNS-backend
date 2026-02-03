from fastapi import Header
from app.crud import users
from fastapi import HTTPException, status

# ユーザーidを取得するための関数
async def authenticate_user(username: str = Header()) -> int:
    user_id = users.get_user_by_username(username).id
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user_id
