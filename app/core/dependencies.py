from fastapi import Header, Depends, HTTPException, status
from crud import users
from db.session import get_db

async def authenticate_user(
    x_username: str = Header(..., alias="X-Username"),
    conn = Depends(get_db)
) -> int:
    """
    リクエストヘッダーからユーザーを認証し、user_idを返す
    
    Args:
        x_username: X-Username ヘッダーの値
        conn: データベース接続
    
    Returns:
        int: ユーザーID
    
    Raises:
        HTTPException: ユーザーが見つからない場合
    """
    user = users.get_user_by_username(conn, x_username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user["id"]
