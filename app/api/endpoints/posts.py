from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.posts import (
    CreatePost,
    GetPostReplies,
    UpdatePost,
    DeletePost,
    ResponsePost,
    ResponsePosts,
    row_to_response_post,
)
from app.db.session import get_db
from app.crud import posts
from app.core.dependencies import authenticate_user

router = APIRouter()

# ==================== Create ====================
@router.post("/", response_model=ResponsePost, status_code=201)
async def create_post(
    post: CreatePost,
    conn=Depends(get_db),
    user_id: int = Depends(authenticate_user)
):
    """投稿を作成する"""
    new_post_id = posts.create_post(
        conn,
        user_id,
        post.content,
        post.reply_to_id,
        post.repost_of_id,
    )
    created_post = posts.get_post_by_id(conn, new_post_id)
    return row_to_response_post(created_post)

# ==================== Read ====================
@router.get("/", response_model=ResponsePosts)
async def get_timeline(
    conn=Depends(get_db),
    user_id: int = Depends(authenticate_user)
):
    """タイムラインを取得する"""
    all_posts = posts.get_all_posts(conn)
    return ResponsePosts(
        posts=[row_to_response_post(p) for p in all_posts],
        total_posts=len(all_posts),
    )

@router.get("/{username}", response_model=ResponsePost)
async def get_own_posts(
    username: str,
    conn=Depends(get_db),
    user_id: int = Depends(authenticate_user)
):
    """ユーザーの投稿を取得する"""
    own_posts = posts.get_posts_by_username(conn, username)
    return ResponsePosts(
        posts=[row_to_response_post(p) for p in own_posts],
        total_posts=len(own_posts),
    )

@router.get("/{post_id}", response_model=ResponsePost)
async def get_post(
    post_id: int,
    conn=Depends(get_db),
    user_id: int = Depends(authenticate_user)
):
    """投稿を取得する"""
    post = posts.get_post_by_id(conn, post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    return row_to_response_post(post)

@router.get("/{post_id}/replies", response_model=ResponsePosts)
async def get_post_replies(
    post_id: int,
    conn=Depends(get_db),
    user_id: int = Depends(authenticate_user)
):
    """投稿への返信を取得する"""
    # 元の投稿が存在するか確認
    original_post = posts.get_post_by_id(conn, post_id)
    if original_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    replies = posts.get_post_replies(conn, post_id)
    return ResponsePosts(
        posts=[row_to_response_post(r) for r in replies],
        total_posts=len(replies),
    )

# ==================== Update ====================
@router.put("/{post_id}", response_model=ResponsePost)
async def update_post(
    post_id: int,
    post: UpdatePost,
    conn=Depends(get_db),
    user_id: int = Depends(authenticate_user)
):
    """投稿を更新する"""
    # 投稿が存在するか確認
    existing_post = posts.get_post_by_id(conn, post_id)
    if existing_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    # 自分の投稿か確認
    if existing_post.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this post"
        )
    
    success = posts.update_post(conn, post_id, post.content)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update post"
        )
    
    updated_post = posts.get_post_by_id(conn, post_id)
    return row_to_response_post(updated_post)

# ==================== Delete ====================
@router.delete("/{post_id}", status_code=204)
async def delete_post(
    post_id: int,
    conn=Depends(get_db),
    user_id: int = Depends(authenticate_user)
):
    """投稿を削除する"""
    # 投稿が存在するか確認
    existing_post = posts.get_post_by_id(conn, post_id)
    if existing_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    # 自分の投稿か確認
    if existing_post.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this post"
        )
    
    success = posts.delete_post(conn, post_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete post"
        )
    
    return None  # 204 No Content