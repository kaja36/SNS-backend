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

# ==================== Update ====================
def update_user(
    conn: sqlite3.Connection,
    user_id: int,
    username: str,
    password_hash: str,
    biography: str,
    avatar_img: str,
) -> bool:
    """
    ユーザーを更新する
    
    Args:
        conn (sqlite3.Connection): データベース接続
        user_id (int): ユーザーID
        username (str): ユーザー名
        password_hash (str): パスワードハッシュ
        biography (str): 自己紹介
        avatar_img (str): アバター画像
    
    Returns:
        bool: 更新成功可否
    """
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users
        SET
            username = ?,
            password_hash = ?,
            biography = ?,
            avatar_img = ?
        WHERE id = ?
    """, (username, password_hash, biography, avatar_img, user_id))
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

# ==================== Others ====================
def prove_user_exists(conn: sqlite3.Connection, username: str, password_hash: str) -> bool:
    """
    ユーザーが存在するかどうかを確認する
    
    Args:
        conn (sqlite3.Connection): データベース接続
        username (str): ユーザー名
        password_hash (str): パスワードハッシュ
    
    Returns:
        bool: ユーザーが存在する場合はTrue、存在しない場合はFalse
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