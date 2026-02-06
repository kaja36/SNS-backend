from fastapi import Header, Depends, HTTPException, status
from app.crud import users
from app.db.session import get_db

async def authenticate_user(
    user_name: str = Header(..., alias="User-name"),
    conn = Depends(get_db)
) -> int:
    """
    リクエストヘッダーからユーザーを認証し、user_idを返す
    
    Args:
        user_name: User_name ヘッダーの値
        conn: データベース接続
    
    Returns:
        int: ユーザーID
    
    Raises:
        HTTPException: ユーザーが見つからない場合
    """
    user = users.get_user_by_username(conn, user_name)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user["id"]
