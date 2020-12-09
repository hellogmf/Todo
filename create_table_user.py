import sqlite3
conn = sqlite3.connect("database.db")
print("Connected to database")
conn.execute("CREATE TABLE user(id INTEGER PRIMARY KEY, username TEXT, password TEXT, firstname TEXT, lastname TEXT, email TEXT, phonenumber INTEGER)")
print("table created successfully")
conn.close()