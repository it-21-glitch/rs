import sqlite3
from threading import local

db = local()


def get_db():
    if not hasattr(db, 'conn'):
        db.conn = sqlite3.connect('RSDataBase.db')
    return db.conn

