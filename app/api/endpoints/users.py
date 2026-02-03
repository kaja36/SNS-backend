from fastapi import APIRouter, HTTPException, status, Depends
from db.session import get_db
from core.dependencies import authenticate_user
from schemas.users import Signup, Login, UpdateUser, UpdatePassword, ResponseUser, ResponseToken, row_to_response_user
from crud import users
from core.password import pwd_context

router = APIRouter()

@router.post("/signup", response_model=ResponseToken, status_code=201)
async def signup(
    user: Signup,
    conn=Depends(get_db),
):
    """ユーザーを新規登録する"""
    # Passwordをハッシュ化
    hashed_password = pwd_context.hash(user.password)
    user_id = users.create_user(conn, user.username, hashed_password)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create user"
        )

    return ResponseToken(
        username=user.username,
    )

@router.post("/login", response_model=ResponseToken)
async def login(
    user: Login,
    conn=Depends(get_db),
):
    """ログインする"""
    registered_user_pw_hash = users.get_user_password_hash_by_username(conn, user.username)

    if registered_user_pw_hash is None or \
      not pwd_context.verify(user.password, registered_user_pw_hash["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    return ResponseToken(
        username=user.username,
    )

@router.post("/logout", status_code=204)
async def logout(
    conn=Depends(get_db),
    user_id: int = Depends(authenticate_user)
):
    """ログアウトする"""
    pass
    

@router.get("/{username}", response_model=ResponseUser)
async def read_user_profile(
    username: str,
    conn=Depends(get_db),
    user_id: int = Depends(authenticate_user)
):
    """ユーザーのプロフィールを取得する"""
    user = users.get_user_by_username(conn, username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return row_to_response_user(user)

@router.put("/me", response_model=ResponseUser)
async def update_user(
    user: UpdateUser,
    conn=Depends(get_db),
    user_id: int = Depends(authenticate_user)
):
    """ユーザーのプロフィールを更新する"""
    new_user = users.update_user(conn, user_id, user.username, user.biography, user.avatar_img)
    if new_user is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user"
        )
    return row_to_response_user(new_user)

@router.put("/me/password", status_code=204)
async def update_password(
    user: UpdatePassword,
    conn=Depends(get_db),
    user_id: int = Depends(authenticate_user)
):
    """ユーザーのパスワードを更新する"""
    # Passwordをハッシュ化
    hashed_password = pwd_context.hash(user.password)
    success = users.update_password(conn, user_id, hashed_password)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update password"
        )
    return None

    
@router.delete("/me", status_code=204)
async def delete_user(
    conn=Depends(get_db),
    user_id: int = Depends(authenticate_user)
):
    """ユーザーを削除する"""
    success = users.delete_user(conn, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user"
        )
    # ログアウトする
