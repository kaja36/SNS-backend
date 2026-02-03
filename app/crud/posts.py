import sqlite3
from core.conf import DEFAULT_LIMIT

# postsテーブルに対するCRUD操作

# ==================== Create ====================
def create_post(
    conn: sqlite3.Connection,
    user_id: int,
    content: str,
    reply_to_id: int | None = None,
    repost_of_id: int | None = None,
) -> int:
    """
    ポストを新規作成する
    
    Args:
        conn (sqlite3.Connection): データベース接続
        user_id (int): ユーザーID
        content (str): ポスト内容
        reply_to_id (int | None, optional): 返信先のポストID。
        repost_of_id (int | None, optional): リポスト元のポストID。
    
    Returns:
        int: 新規作成されたポストのID
    """
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO posts (user_id, content, reply_to_id, repost_of_id)
        VALUES (?, ?, ?, ?)
    """, (user_id, content, reply_to_id, repost_of_id))
    conn.commit()
    return cursor.lastrowid

# ==================== Read ====================
def get_all_posts(
        conn: sqlite3.Connection,
        limit: int = DEFAULT_LIMIT,
    ) -> list[tuple]:
    """
    全てのポストを取得する
    
    Args:
        conn (sqlite3.Connection): データベース接続
        limit (int, optional): 取得件数。デフォルトはDEFAULT_LIMIT。
    
    Returns:
        list[tuple]: 全てのポストのリスト
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT
            id,
            user_id,
            content,
            reply_to_id,
            repost_of_id,
            created_at
        FROM posts
        ORDER BY created_at DESC
        LIMIT ?
        """,
        (limit,)
    )
    return cursor.fetchall()

def get_post_by_id(
        conn: sqlite3.Connection,
        post_id: int,
    ) -> tuple | None:
    """
    IDでポストを取得する
    
    Args:
        conn (sqlite3.Connection): データベース接続
        post_id (int): ポストID
    
    Returns:
        tuple | None: ポストのタプル。存在しない場合はNone。
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT
            id,
            user_id,
            content,
            reply_to_id,
            repost_of_id,
            created_at
        FROM posts
        WHERE id = ?
        """,
        (post_id,)
    )
    return cursor.fetchone()

def get_posts_by_user_id(
        conn: sqlite3.Connection,
        user_id: int,
        limit: int = DEFAULT_LIMIT,
    ) -> list[tuple]:
    """
    ユーザーIDでポストを取得する
    
    Args:
        conn (sqlite3.Connection): データベース接続
        user_id (int): ユーザーID
        limit (int, optional): 取得件数。デフォルトはDEFAULT_LIMIT。
    
    Returns:
        list[tuple]: ユーザーIDで取得したポストのリスト
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT
            id,
            user_id,
            content,
            reply_to_id,
            repost_of_id,
            created_at
        FROM posts
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT ?
        """,
        (user_id, limit)
    )
    return cursor.fetchall()

# def get_posts_by_following_users(
#         conn: sqlite3.Connection,
#         user_id: int,
#         limit: int = DEFAULT_LIMIT,
#     ) -> list[tuple]:
#     """
#     ユーザーがフォローしているユーザーのポストを取得する
    
#     Args:
#         conn: データベース接続
#         user_id: ユーザーID
    
#     Returns:
#         ユーザーがフォローしているユーザーのポストのリスト
#     """
#     cursor = conn.cursor()
#     cursor.execute("""
#         SELECT * 
#         FROM 
#             posts as p
#         JOIN
#             follows as f
#         ON 
#             p.user_id = f.following_id
#         WHERE 
#             f.follower_id = ?
#         ORDER BY 
#             p.created_at DESC 
#         LIMIT ?
#     """, (user_id, limit))
#     return cursor.fetchall()

# ==================== Update ====================
def update_post(
        conn: sqlite3.Connection,
        post_id: int,
        content: str,
    ) -> bool:
    """
    ポストを更新する
    
    Args:
        conn (sqlite3.Connection): データベース接続
        post_id (int): ポストID
        content (str): ポスト内容
    
    Returns:
        bool: 更新成功可否
    """
    cursor = conn.cursor()
    cursor.execute("UPDATE posts SET content = ? WHERE id = ?", (content, post_id))
    conn.commit()
    return cursor.rowcount > 0

# ==================== Delete ====================
def delete_post(
        conn: sqlite3.Connection,
        post_id: int,
    ) -> bool:
    """
    ポストを削除する
    
    Args:
        conn (sqlite3.Connection): データベース接続
        post_id (int): ポストID
    
    Returns:
        bool: 削除成功可否
    """
    cursor = conn.cursor()
    cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    return cursor.rowcount > 0