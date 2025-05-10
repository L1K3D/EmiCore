import duckdb
conn = duckdb.connect("teste.db")
conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT);")
print("Database created successfully!")