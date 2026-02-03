import sqlite3

# usersテーブルに対するCRUD操作
# ==================== Create ====================
def create_user(
    conn: sqlite3.Connection,
    username: str,
    password_hash: str,
    biography: str = "",
    avatar_img: str = "",
) -> int:
    """
    ユーザーを作成する
    
    Args:
        conn (sqlite3.Connection): データベース接続
        username (str): ユーザー名
        password_hash (str): パスワードハッシュ
        biography (str, optional): 自己紹介。デフォルトは空文字列。
        avatar_img (str, optional): アバター画像。デフォルトは空文字列。
    
    Returns:
        int: 作成されたユーザーのID
    """
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (
            username,
            password_hash,
            biography,
            avatar_img
        ) VALUES (?, ?, ?, ?)
    """, (username, password_hash, biography, avatar_img))
    # データを保存
    conn.commit()
    return cursor.lastrowid

# ==================== Read ====================
def get_all_users(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    """
    全てのユーザーの公開情報を取得する
    
    Args:
        conn (sqlite3.Connection): データベース接続
    
    Returns:
        list[sqlite3.Row]: 全てのユーザーのタプルリスト
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT
            id,
            username,
            biography,
            avatar_img,
            created_at
        FROM users
        """
    )
    return cursor.fetchall()

def get_user_by_id(conn: sqlite3.Connection, user_id: int) -> sqlite3.Row | None:
    """
    IDでユーザーの公開情報を取得する
    
    Args:
        conn (sqlite3.Connection): データベース接続
        user_id (int): ユーザーID
    
    Returns:
        sqlite3.Row | None: ユーザーのタプル。存在しない場合はNone。
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT
            id,
            username,
            biography,
            avatar_img,
            created_at
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    )
    return cursor.fetchone()

def get_user_by_username(conn: sqlite3.Connection, username: str) -> sqlite3.Row | None:
    """
    ユーザー名でユーザーの公開情報を取得する
    
    Args:
        conn (sqlite3.Connection): データベース接続
        username (str): ユーザー名
    
    Returns:
        sqlite3.Row | None: ユーザーのタプル。存在しない場合はNone。
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT
            id,
            username,
            biography,
            avatar_img,
            created_at
        FROM users
        WHERE username = ?
        """,
        (username,)
    )
    return cursor.fetchone()

def get_user_password_hash_by_username(
    conn: sqlite3.Connection,
    username: str
) -> sqlite3.Row | None:
    """
    ユーザー名でユーザーのパスワードハッシュを取得する
    
    Args:
        conn (sqlite3.Connection): データベース接続
        username (str): ユーザー名
    
    Returns:
        sqlite3.Row | None: パスワードハッシュのタプル。存在しない場合はNone。
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT
            password_hash
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
    biography: str,
    avatar_img: str,
) -> sqlite3.Row | None:
    """
    ユーザーを更新する
    
    Args:
        conn (sqlite3.Connection): データベース接続
        user_id (int): ユーザーID
        username (str): ユーザー名
        biography (str): 自己紹介
        avatar_img (str): アバター画像
    
    Returns:
        sqlite3.Row | None: 更新されたユーザーのタプル。存在しない場合はNone。
    """
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users
        SET
            username = ?,
            biography = ?,
            avatar_img = ?
        WHERE id = ?
        RETURNING 
            id,
            username,
            biography,
            avatar_img,
            created_at
    """, (username, biography, avatar_img, user_id))
    result = cursor.fetchone()
    conn.commit()
    return result

def update_password(
    conn: sqlite3.Connection,
    user_id: int,
    password_hash: str,
) -> bool:
    """
    パスワードを更新する
    
    Args:
        conn (sqlite3.Connection): データベース接続
        user_id (int): ユーザーID
        password_hash (str): パスワードハッシュ
    
    Returns:
        bool: 更新成功可否
    """
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users
        SET
            password_hash = ?
        WHERE id = ?
    """, (password_hash, user_id))
    conn.commit()
    return cursor.rowcount > 0

# ==================== Delete ====================
def delete_user(conn: sqlite3.Connection, user_id: int) -> bool:
    """
    ユーザーを削除する
    
    Args:
        conn (sqlite3.Connection): データベース接続
        user_id (int): ユーザーID
    
    Returns:
        bool: 削除成功可否
    """
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM users
        WHERE id = ?
    """, (user_id,))
    conn.commit()
    return cursor.rowcount > 0
