import sqlite3 
from random import randint
from usuario import Usuarios

class UsuarioRepository:
    def __init__(self):
        # Cria a tabela e fecha. 
        with self.conectar() as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS usuarios(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conta INTEGER UNIQUE,
                nome TEXT,
                sobrenome TEXT,
                email TEXT UNIQUE,
                login TEXT UNIQUE,
                senha TEXT,
                saldo REAL DEFAULT 0)""")

    def conectar(self):
        return sqlite3.connect("banco_dados.db", timeout=10)

    def _buscar_usuario(self, query, params):
        with self.conectar() as conn:
            cursor = conn.cursor()
            # Buscamos as colunas na ordem exata do construtor da classe Usuarios
            cursor.execute(f"SELECT nome, sobrenome, email, login, senha, saldo, conta FROM usuarios WHERE {query}", params)
            dados = cursor.fetchone()
            return Usuarios(*dados) if dados else None

    def buscar_por_login(self, login):
        return self._buscar_usuario("login = ?", (login,))

    def buscar_por_email(self, email):
        return self._buscar_usuario("email = ?", (email,))
    
    def cadastrar(self, usuario):
        with self.conectar() as conn:
            cursor = conn.cursor()
            while True:
                gerar_conta = randint(1000, 9999)
                # Verifica se a conta já existe
                cursor.execute("SELECT 1 FROM usuarios WHERE conta = ?", (gerar_conta,))
                if not cursor.fetchone():
                    cursor.execute("""INSERT INTO usuarios
                        (conta, nome, sobrenome, email, login, senha, saldo) 
                        VALUES (?,?,?,?,?,?,?)""",
                        (gerar_conta, usuario.nome, usuario.sobrenome, usuario.email, 
                         usuario.login, usuario.senha, usuario.saldo))
                    conn.commit()
                    break

    def busca_saldo(self, conta):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT saldo FROM usuarios WHERE conta=?", (conta,))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else 0

    def atualizar_saldo(self, conta, valor):
        with self.conectar() as conn:
            conn.execute("UPDATE usuarios SET saldo =? WHERE conta=?", (valor, conta))
            conn.commit()