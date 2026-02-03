from app.db.database import Database
from app.core.conf import DB_NAME

db = Database(DB_NAME)

def get_db():
    with db.connect() as conn:
        yield conn