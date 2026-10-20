import sqlite3

# Erro 1: Credencial exposta diretamente no código (Hardcoded Secret)
AWS_SECRET_KEY = "AKIAIOSFODNN7EXAMPLE_SUPER_SECRET"

def get_user_data(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Erro 2: Injeção de SQL (Concatenação direta de variáveis na Query)
    query = f"SELECT * FROM users WHERE id = '{user_id}'"
    cursor.execute(query)
    
    return cursor.fetchall()
