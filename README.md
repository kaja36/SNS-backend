## データベース設計

```mermaid
erDiagram
    users ||--o{ posts : creates
    users ||--o{ follows : follower
    users ||--o{ follows : following
    users ||--o{ likes : gives
    posts ||--o{ likes : receives
    posts ||--o{ posts : reply_to

    users {
        int id PK
        string username UK
        string email UK
        string password_hash
        string biograpy
        string avatar_url
        datetime created_at
    }

    posts {
        int id PK
        int user_id FK
        string content
        int reply_to_id FK
        int repost_of_id FK
        datetime created_at
    }

    follows {
        int follower_id FK
        int following_id FK
        datetime created_at
    }

    likes {
        int user_id FK
        int post_id FK
        datetime created_at
    }
```

---

## API仕様

### 認証

リクエストヘッダーに `X-Username` を設定：

```
X-Username: <username>
```

> 将来的には `Authorization: Bearer <token>` に置き換え予定

---

### Users API

#### POST `/users/signup` - ユーザー登録

| 項目       | 値          |
| ---------- | ----------- |
| 認証       | 不要        |
| ステータス | 201 Created |

**リクエスト:**

```json
{
  "username": "string",
  "password": "string"
}
```

**レスポンス:**

```json
{
  "username": "string"
}
```

---

#### POST `/users/login` - ログイン

| 項目       | 値     |
| ---------- | ------ |
| 認証       | 不要   |
| ステータス | 200 OK |

**リクエスト:**

```json
{
  "username": "string",
  "password": "string"
}
```

**レスポンス:**

```json
{
  "username": "string"
}
```

---

#### GET `/users/{username}` - プロフィール取得

| 項目       | 値     |
| ---------- | ------ |
| 認証       | 必要   |
| ステータス | 200 OK |

**パスパラメータ:**

- `username`: ユーザー名

**レスポンス:**

```json
{
  "username": "string",
  "biography": "string",
  "avatar_img": "string",
  "created_at": "datetime"
}
```

---

#### PUT `/users/me` - プロフィール更新

| 項目       | 値     |
| ---------- | ------ |
| 認証       | 必要   |
| ステータス | 200 OK |

**リクエスト:**

```json
{
  "username": "string",
  "biography": "string",
  "avatar_img": "string"
}
```

**レスポンス:**

```json
{
  "username": "string",
  "biography": "string",
  "avatar_img": "string",
  "created_at": "datetime"
}
```

---

#### PUT `/users/me/password` - パスワード更新

| 項目       | 値             |
| ---------- | -------------- |
| 認証       | 必要           |
| ステータス | 204 No Content |

**リクエスト:**

```json
{
  "password": "string"
}
```

---

#### DELETE `/users/me` - アカウント削除

| 項目       | 値             |
| ---------- | -------------- |
| 認証       | 必要           |
| ステータス | 204 No Content |

---

### Posts API

#### POST `/posts/` - 投稿作成

| 項目       | 値          |
| ---------- | ----------- |
| 認証       | 必要        |
| ステータス | 201 Created |

**リクエスト:**

```json
{
  "content": "string",
  "reply_to_id": "int | null",
  "repost_of_id": "int | null"
}
```

**レスポンス:**

```json
{
  "post_id": "int",
  "username": "string",
  "content": "string",
  "avatar_img": "string",
  "created_at": "datetime",
  "reply_to_id": "int | null",
  "repost_of_id": "int | null",
  "repost_of_content": "string | null",
  "reply_count": "int",
  "repost_count": "int",
  "like_count": "int",
  "is_following": "boolean",
  "is_liked": "boolean"
}
```

---

#### GET `/posts/` - タイムライン取得

| 項目       | 値     |
| ---------- | ------ |
| 認証       | 必要   |
| ステータス | 200 OK |

**レスポンス:**

```json
{
  "posts": [ResponsePost],
  "total_posts": "int"
}
```

---

#### GET `/posts/{post_id}` - 投稿取得

| 項目       | 値     |
| ---------- | ------ |
| 認証       | 必要   |
| ステータス | 200 OK |

**パスパラメータ:**

- `post_id`: 投稿ID

---

#### GET `/posts/{post_id}/replies` - リプライ取得

| 項目       | 値     |
| ---------- | ------ |
| 認証       | 必要   |
| ステータス | 200 OK |

**パスパラメータ:**

- `post_id`: 投稿ID

**レスポンス:**

```json
{
  "posts": [ResponsePost],
  "total_posts": "int"
}
```

---

#### PUT `/posts/{post_id}` - 投稿更新

| 項目       | 値                     |
| ---------- | ---------------------- |
| 認証       | 必要（自分の投稿のみ） |
| ステータス | 200 OK                 |

**パスパラメータ:**

- `post_id`: 投稿ID

**リクエスト:**

```json
{
  "content": "string"
}
```

---

#### DELETE `/posts/{post_id}` - 投稿削除

| 項目       | 値                     |
| ---------- | ---------------------- |
| 認証       | 必要（自分の投稿のみ） |
| ステータス | 204 No Content         |

**パスパラメータ:**

- `post_id`: 投稿ID

---

### Swagger UI

```
http://localhost:8000/docs
```

---

## 技術スタック

| カテゴリ       | 技術                            |
| -------------- | ------------------------------- |
| フレームワーク | FastAPI                         |
| データベース   | sqlite3（Python標準ライブラリ） |
| バリデーション | Pydantic v2                     |

---

## セットアップ

```bash
# 仮想環境の作成
python -m venv venv
source venv/bin/activate

# 依存関係のインストール
pip install -r requirements.txt

# サーバー起動
uvicorn app.main:app --reload
```
