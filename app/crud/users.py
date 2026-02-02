import sqlite3

# usersテーブルに対するCRUD操作
# ==================== Create ====================
def create_user(
    conn: sqlite3.Connection,
    username: str,
    password_hash: str,
    biography: str = "",
    avatar_url: str = "",
) -> int:
    """
    ユーザーを作成する
    
    Args:
        conn: データベース接続
        username: ユーザー名
        password_hash: パスワードハッシュ
        biography: 自己紹介（デフォルトは空文字列）
        avatar_url: アバターURL（デフォルトは空文字列）
    
    Returns:
        作成されたユーザーのID
    """
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (
            username,
            password_hash,
            biography,
            avatar_url
        ) VALUES (?, ?, ?, ?)
    """, (username, password_hash, biography, avatar_url))
    # データを保存
    conn.commit()
    return cursor.lastrowid

# ==================== Read ====================
def get_all_users(conn: sqlite3.Connection) -> list[tuple]:
    """
    全てのユーザーを取得する
    
    Args:
        conn: データベース接続
    
    Returns:
        全てのユーザーのタプルリスト
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT
            id,
            username,
            biography,
            avatar_url,
            created_at
        FROM users
        """
    )
    return cursor.fetchall()

def get_user_by_id(conn: sqlite3.Connection, user_id: int) -> tuple | None:
    """
    IDでユーザーを取得する
    
    Args:
        conn: データベース接続
        user_id: ユーザーID
    
    Returns:
        ユーザーのタプル、またはNone
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT
            id,
            username,
            biography,
            avatar_url,
            created_at
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    )
    return cursor.fetchone()

def get_user_by_username(conn: sqlite3.Connection, username: str) -> tuple | None:
    """
    ユーザー名でユーザーを取得する
    
    Args:
        conn: データベース接続
        username: ユーザー名
    
    Returns:
        ユーザーのタプル、またはNone
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT
            id,
            username,
            biography,
            avatar_url,
            created_at
        FROM users
        WHERE username = ?
        """,
        (username,)
    )
    return cursor.fetchone()

# ==================== Update ====================
def update_user(
    conn: sqlite3.Connection,
    user_id: int,
    username: str,
    password_hash: str,
    biography: str,
    avatar_url: str,
) -> bool:
    """
    ユーザーを更新する
    
    Args:
        conn: データベース接続
        user_id: ユーザーID
        username: ユーザー名
        password_hash: パスワードハッシュ
        biography: 自己紹介
        avatar_url: アバターURL
    
    Returns:
        更新成功可否
    """
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users
        SET
            username = ?,
            password_hash = ?,
            biography = ?,
            avatar_url = ?
        WHERE id = ?
    """, (username, password_hash, biography, avatar_url, user_id))
    conn.commit()
    return cursor.rowcount > 0

# ==================== Delete ====================
def delete_user(conn: sqlite3.Connection, user_id: int) -> bool:
    """
    ユーザーを削除する
    
    Args:
        conn: データベース接続
        user_id: ユーザーID
    
    Returns:
        削除成功可否
    """
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM users
        WHERE id = ?
    """, (user_id,))
    conn.commit()
    return cursor.rowcount > 0

# ==================== Others ====================
def prove_user_exists(conn: sqlite3.Connection, username: str, password_hash: str) -> bool:
    """
    ユーザーが存在するかどうかを確認する
    
    Args:
        conn: データベース接続
        username: ユーザー名
        password_hash: パスワードハッシュ
    
    Returns:
        ユーザーが存在する場合はTrue、存在しない場合はFalse
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT EXISTS(
            SELECT 1 FROM users WHERE username = ? AND password_hash = ?
        )
        """, 
        (username, password_hash)
    )
    return cursor.fetchone()[0] == 1