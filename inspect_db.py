import sqlite3
from pathlib import Path

# Path to the database file (adjust if needed)
db_path = Path(__file__).resolve().parent / "test.db"

# Connect to SQLite DB
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get list of tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print(f"\nTables in {db_path}:")
for table in tables:
    print(f"- {table[0]}")

cursor.close()
conn.close()
