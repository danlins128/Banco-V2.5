import sqlite3 

class UsuarioRepository:
	def __init__(self):
		self.conn = sqlite3.connect("banco_dados.db")
		self.cursor = self.conn.cursor()
		
		self.cursor.execute("""CREATE TABLE IF 				NOT EXISTS usuarios(id INTEGER 						PRIMARY KEY AUTOINCREMENT,
			nome TEXT,
			login TEXT UNIQUE,
			senha TEXT UNIQUE,
			saldo REAL)""")
		self.conn.commit()
		
	def buscar_por_login(self, login):
	  self.cursor.execute("SELECT nome, login, senha FROM usuario WHERE login = ?",
	  (login))
	  dados = self.cursor.fetchone()
	  if dados:
	    return Usuario(*dados)
	  return None
	
	def cadastrar(self, usuario):
	  self.cursor.execute("INSERT INTO usuario (nome, login, senha), VALUES (?, ?, ?)"
	  (usuario.nome, usuario.login, usuario.senha))
	  self.conn.commit()
	
conexao=UsuarioRepository()
conexao.conn.close()