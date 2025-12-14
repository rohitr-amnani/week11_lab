import sqlite3
import pandas as pd
from pathlib import Path

class DatabaseManager:
    def __init__(self, db_path=None):
        if db_path is None:
            self.db_path = Path(__file__).parent / "intelligence_platform.db"
        else:
            self.db_path = Path(db_path)

    #get database connection method
    def get_connection(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        return sqlite3.connect(str(self.db_path))

    #execute query method
    def execute_query(self, query, params=()):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        last_id = cursor.lastrowid
        row_count = cursor.rowcount
        conn.close()
        return last_id, row_count

    #fetch data method
    def fetch_data(self, query, params=()):
        conn = self.get_connection()
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df