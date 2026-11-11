import sqlite3

class TriangleDatabase:

    def __init__(self, db_path=":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS triangles (
                a REAL NOT NULL,
                b REAL NOT NULL,
                c REAL NOT NULL,
                type TEXT NOT NULL,
                error TEXT,
                PRIMARY KEY (a, b, c)
            )
        """)
        self.conn.commit()

    def add(self, a, b, c, t, error=""):
        self.conn.execute(
            "INSERT OR REPLACE INTO triangles (a, b, c, type, error) VALUES (?, ?, ?, ?, ?)",
            (float(a), float(b), float(c), t, error)
        )
        self.conn.commit()

    def get(self, a, b, c):
        cur = self.conn.execute(
            "SELECT type, error FROM triangles WHERE a=? AND b=? AND c=?",
            (float(a), float(b), float(c))
        )
        row = cur.fetchone()
        return (row["type"], row["error"]) if row else None

    def delete(self, a, b, c):
        self.conn.execute(
            "DELETE FROM triangles WHERE a=? AND b=? AND c=?",
            (float(a), float(b), float(c))
        )
        self.conn.commit()

    def close(self):
        self.conn.close()