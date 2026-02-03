from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# ==================== Request ====================
# ============ Create ============
class CreatePost(BaseModel):
    content: str
    reply_to_id: Optional[int] = None
    repost_of_id: Optional[int] = None

# ============ Update ============
class UpdatePost(BaseModel):
    post_id: int
    content: str

# ============ Delete ============
class DeletePost(BaseModel):
    post_id: int


# ==================== Response ====================
class ResponsePost(BaseModel):
    """
    1ポストのレスポンス構造
    
    post_id (int) : ポストID
    username (str) : ユーザー名
    content (str) : ポスト内容
    avatar_img (str) : アバター画像
    is_following (bool) : フォローしているかどうか
    created_at (datetime) : 作成日時
    repost_count (int, optional) : リポスト数
    like_count (int, optional) : いいね数
    reply_count (int, optional) : 返信数
    is_liked (bool, optional) : いいねしているかどうか
    repost_of_id (int, optional) : リポスト元のポストID
    repost_of_content (str, optional) : リポスト元のポスト内容
    """
    post_id: int
    username: str
    content: str
    avatar_img: str
    is_following: bool
    created_at: datetime
    repost_count: Optional[int]
    like_count: Optional[int]
    reply_count: Optional[int]
    is_liked: Optional[bool]
    repost_of_id: Optional[int]
    repost_of_content: Optional[str]

class ResponsePosts(BaseModel):
    posts: list[ResponsePost]
    total_posts: int


# ==================== OTHER ====================
import sqlite3

def row_to_response_post(row: sqlite3.Row) -> ResponsePost:
    return ResponsePost(
        post_id=row["post_id"],
        username=row["username"],
        content=row["content"],
        avatar_img=row["avatar_img"],
        is_following=False,
        created_at=row["created_at"],
        repost_count=row["repost_count"],
        like_count=0,
        reply_count=row["reply_count"],
        is_liked=False,
        repost_of_id=row["repost_of_id"],
        repost_of_content=row["repost_of_content"],
    )