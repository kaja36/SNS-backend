import sqlite3
from app.core.conf import DEFAULT_LIMIT

# postsテーブルに対するCRUD操作

# ==================== 共通SQL ====================
# ResponsePost に合わせたSELECT句（JOINあり）
# テーブル追加時はここを変更するだけでOK
BASE_SELECT_POSTS = """
    SELECT
        p.id AS post_id,
        u.username,
        p.content,
        u.avatar_img,
        p.created_at,
        p.reply_to_id,
        p.repost_of_id,
        rp.content AS repost_of_content,
        (SELECT COUNT(*) FROM posts WHERE reply_to_id = p.id) AS reply_count,
        (SELECT COUNT(*) FROM posts WHERE repost_of_id = p.id) AS repost_count
    FROM posts p
    JOIN users u ON p.user_id = u.id
    LEFT JOIN posts rp ON p.repost_of_id = rp.id
"""

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
    ) -> list[sqlite3.Row]:
    """
    全てのポストを取得する（JOINでユーザー情報含む）
    
    Args:
        conn (sqlite3.Connection): データベース接続
        limit (int, optional): 取得件数。デフォルトはDEFAULT_LIMIT。
    
    Returns:
        list[sqlite3.Row]: 全てのポストのリスト
    """
    cursor = conn.cursor()
    cursor.execute(
        BASE_SELECT_POSTS + """
        ORDER BY p.created_at DESC
        LIMIT ?
        """,
        (limit,)
    )
    return cursor.fetchall()

def get_post_by_id(
        conn: sqlite3.Connection,
        post_id: int,
    ) -> sqlite3.Row | None:
    """
    IDでポストを取得する（JOINでユーザー情報含む）
    
    Args:
        conn (sqlite3.Connection): データベース接続
        post_id (int): ポストID
    
    Returns:
        sqlite3.Row | None: ポストのタプル。存在しない場合はNone。
    """
    cursor = conn.cursor()
    cursor.execute(
        BASE_SELECT_POSTS + """
        WHERE p.id = ?
        """,
        (post_id,)
    )
    return cursor.fetchone()

def get_posts_by_user_id(
        conn: sqlite3.Connection,
        user_id: int,
        limit: int = DEFAULT_LIMIT,
    ) -> list[sqlite3.Row]:
    """
    ユーザーIDでポストを取得する（JOINでユーザー情報含む）
    
    Args:
        conn (sqlite3.Connection): データベース接続
        user_id (int): ユーザーID
        limit (int, optional): 取得件数。デフォルトはDEFAULT_LIMIT。
    
    Returns:
        list[sqlite3.Row]: ユーザーIDで取得したポストのリスト
    """
    cursor = conn.cursor()
    cursor.execute(
        BASE_SELECT_POSTS + """
        WHERE p.user_id = ?
        ORDER BY p.created_at DESC
        LIMIT ?
        """,
        (user_id, limit)
    )
    return cursor.fetchall()

def get_post_replies(
        conn: sqlite3.Connection,
        post_id: int,
        limit: int = DEFAULT_LIMIT,
    ) -> list[sqlite3.Row]:
    """
    ポストへの返信を取得する（JOINでユーザー情報含む）
    
    Args:
        conn (sqlite3.Connection): データベース接続
        post_id (int): ポストID
        limit (int, optional): 取得件数。デフォルトはDEFAULT_LIMIT。
    
    Returns:
        list[sqlite3.Row]: 返信ポストのリスト
    """
    cursor = conn.cursor()
    cursor.execute(
        BASE_SELECT_POSTS + """
        WHERE p.reply_to_id = ?
        ORDER BY p.created_at DESC
        LIMIT ?
        """,
        (post_id, limit)
    )
    return cursor.fetchall()

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