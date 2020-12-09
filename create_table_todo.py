import sqlite3
conn = sqlite3.connect("database.db")
print("Connected to database")
conn.execute("CREATE TABLE todo(id INTEGER PRIMARY KEY, task_name TEXT, priority TEXT , status TEXT)")
print("table created successfully")
conn.close()