import sqlite3

def init_db():
    conn = sqlite3.connect('comentarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comentarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            comentario TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def salvar_comentario(nome, comentario):
    conn = sqlite3.connect('comentarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO comentarios (nome, comentario)
        VALUES (?, ?)
    ''', (nome, comentario))
    conn.commit()
    conn.close()

def carregar_comentarios():
    conn = sqlite3.connect('comentarios.db')
    cursor = conn.cursor()
    cursor.execute('SELECT nome, comentario FROM comentarios ORDER BY id DESC')
    comentarios = cursor.fetchall()
    conn.close()
    return comentarios
