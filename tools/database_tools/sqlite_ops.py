import sqlite3
from tools.base import Tool

class SQLiteQueryTool(Tool):
    def __init__(self):
        super().__init__(name="sqlite_query", description="Ejecuta una consulta SQL en una base de datos SQLite")

    def execute(self, db_path, query, params=None):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if query.strip().upper().startswith("SELECT"):
                results = cursor.fetchall()
                conn.close()
                return results
            else:
                conn.commit()
                rowcount = cursor.rowcount
                conn.close()
                return f"Consulta ejecutada. Filas afectadas: {rowcount}"
        except Exception as e:
            return f"Error en SQLite: {str(e)}"
