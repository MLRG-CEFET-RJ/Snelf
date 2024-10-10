import sqlite3
from infra.DBConnection import DBConnection
import traceback

class BaseDAO:
    def __init__(self):
        self.db = DBConnection()
    
    def iniciar_transacao_db(self):
        self.db.connection.autocommit = False

    def commit_transacao_db(self):
        self.db.connection.commit()
        self.db.connection.autocommit = True

    def rollback_transacao_db(self):
        self.db.connection.rollback()
        self.db.connection.autocommit = True

    def select(self, query, params=None):
        cursor = self.db.cursor
        cursor.execute(query, params)
        return cursor.fetchall()

    def insert(self, query, params):
        cursor = self.db.cursor
        cursor.execute(query, params)
        self.db.connection.commit()

    def delete(self, query, params):
        cursor = self.db.cursor
        cursor.execute(query, params)
        self.db.connection.commit()

    def update(self, query, params):
        cursor = self.db.cursor
        cursor.execute(query, params)
        self.db.connection.commit()