import sqlite3

banco = sqlite3.connect(r"..\controle_refugo\data\dados.db")
cursor = banco.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS auth (username text, password text)")