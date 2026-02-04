from .database import Database
from core.conf import DB_NAME

db = Database(DB_NAME)

def get_db():
    with db.connect() as conn:
        yield conn