class Banco:
	def __init__(self):
		self.usuarios=[]
		
	def adicionar_usuarios(self, usuario):
		self.usuarios.append(usuario)
		print("Usuário Cadastrado com sucesso!\n")
		
	def buscar_usuario(self, login):
		for usuario in self.usuarios:
			if usuario.login==login:
				return usuario
		return None
