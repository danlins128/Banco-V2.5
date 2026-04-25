import sqlite3 
from random import randint
from usuario import Usuarios

class UsuarioRepository:
    def __init__(self):
        self.conn = sqlite3.connect("banco_dados.db", check_same_thread=False)
        self.cursor = self.conn.cursor()

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conta INTEGER UNIQUE,
            nome TEXT,
            sobrenome TEXT,
            email TEXT UNIQUE,
            login TEXT UNIQUE,
            senha TEXT,
            saldo REAL DEFAULT 0)""")
        self.conn.commit()

    def buscar_por_login(self, login):
      self.cursor.execute("""SELECT nome, sobrenome, email, login, senha, saldo, conta FROM usuarios WHERE login =
      ?""",
      (login,))
      dados = self.cursor.fetchone()
      if dados:
          return Usuarios(*dados)
      return None

    def cadastrar(self, usuario):
      while True:
          gerar_conta = randint (1000,9999)
          self.cursor.execute("""SELECT conta FROM usuarios WHERE conta=?""",
          (gerar_conta,))
          resultado = self.cursor.fetchone()
          if resultado is None:
              self.cursor.execute("""INSERT INTO usuarios
              (conta, nome, sobrenome, email, login, senha, saldo) VALUES (?,?,?,?,?,?,?)""",
              (gerar_conta, usuario.nome, usuario.sobrenome, usuario.email, usuario.login, usuario.senha,
              usuario.saldo))
              self.conn.commit()
              break
          
    def busca_saldo(self, conta):
        self.cursor.execute("""
        SELECT saldo FROM usuarios WHERE conta=?""", (conta,))
        resultado = self.cursor.fetchone()
        return resultado [0] if resultado else 0

    def atualizar_saldo(self, conta, valor):
        self.cursor.execute("""UPDATE usuarios SET saldo =? WHERE conta=?""", (valor,conta))
        self.conn.commit()


        

