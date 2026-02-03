import sqlite3
from contextlib import contextmanager
from app.core.conf import DB_BASE_PATH

class Database:
    def __init__(self, db_name: str):
        self.db_name = DB_BASE_PATH + db_name

    @contextmanager
    def connect(self):
        """
        データベースへの接続を開き、使用後に自動で閉じるコンテキストマネージャー
        
        with文で使用することで、処理完了後に自動的にconnection.close()が呼ばれる。
        DBファイルが存在しない場合は新規作成される。

        Yields:
            sqlite3.Connection: データベースへの接続
        
        Raises:
            sqlite3.Error: データベース接続エラー
        
        Example:
            with db.connect() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users")
        """
        conn = self.get_connection()
        try:
            yield conn
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise
        finally:
            print(f"closing connection to {self.db_name}")
            conn.close()

    def get_connection(self) -> sqlite3.Connection:
        """
        DBに接続する
        DBファイルが存在しない場合は新規作成される。
        with文を使わない場合は、呼び出し側でclose()を呼ぶ必要がある。

        Returns:
            sqlite3.Connection: データベースへの接続
        Example:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            conn.close()
        """
        print(f"getting connection to {self.db_name}")
        conn = sqlite3.connect(self.db_name, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self) -> None:
        """
        データベースを初期化する
        
        usersテーブルとpostsテーブルを作成する。
        テーブルが既に存在する場合は何もしない。
        """
        with self.connect() as conn:
            try:
                cursor = conn.cursor()
                # テーブルの作成
                # usersテーブル
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id              INTEGER     PRIMARY KEY,
                        username        TEXT        NOT NULL UNIQUE,
                        password_hash   TEXT        NOT NULL,
                        biography       TEXT        DEFAULT "",
                        avatar_img      TEXT        DEFAULT "",
                        created_at      DATETIME    DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                # postsテーブル
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS posts (
                        id              INTEGER     PRIMARY KEY,
                        user_id         INTEGER     NOT NULL,
                        content         TEXT        NOT NULL,
                        reply_to_id     INTEGER     DEFAULT NULL,
                        repost_of_id    INTEGER     DEFAULT NULL,
                        created_at      DATETIME    DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id),
                        FOREIGN KEY (reply_to_id) REFERENCES posts(id),
                        FOREIGN KEY (repost_of_id) REFERENCES posts(id)
                    )
                """)
                # # likesテーブル
                # cursor.execute("""
                #     CREATE TABLE IF NOT EXISTS likes (
                #         user_id         INTEGER     NOT NULL,
                #         post_id         INTEGER     NOT NULL,
                #         created_at      DATETIME    DEFAULT CURRENT_TIMESTAMP,
                #         FOREIGN KEY (user_id) REFERENCES users(id),
                #         FOREIGN KEY (post_id) REFERENCES posts(id),
                #         PRIMARY KEY (user_id, post_id)
                #     )
                # """)
                # # followsテーブル
                # cursor.execute("""
                #     CREATE TABLE IF NOT EXISTS follows (
                #         follower_id     INTEGER     NOT NULL,
                #         following_id    INTEGER     NOT NULL,
                #         created_at      DATETIME    DEFAULT CURRENT_TIMESTAMP,
                #         PRIMARY KEY (follower_id, following_id),
                #         FOREIGN KEY (follower_id) REFERENCES users(id),
                #         FOREIGN KEY (following_id) REFERENCES users(id)
                #     )
                # """)

                # トランザクションのコミット
                conn.commit()
            except sqlite3.Error as e:
                print(f"Error initializing database: {e}")
                raise
        