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
		
class ContaService:
	def __init__(self, banco):
		self.banco = banco	
		
	def depositar(self, login, valor):
		usuario = self.banco.buscar_usuario(login)
		if usuario is None:
			print("Usuário inválido ou não cadastrado.")
			return
		if valor <= 0:
			print("Valor indefinido !")
			return
		usuario.saldo += valor
		print(f"Depósito de {valor:,.2f} efetuado com sucesso\n")
		print(f"Novo saldo atual de {usuario.nome}, R$ {usuario.saldo}.")
				
	def sacar(self, login, valor):
		cliente = self.banco.buscar_usuario(login)
		if cliente is None:
			print("Usuário não cadastrado, ou não encontrado\n")
			return
		if cliente.saldo < valor:
			print("Valor insuficiente para saque\n")
			return 
		if valor <= 0:
			print("Erro!\n")
			return
		cliente.saldo -= valor
		print(f"Saque de {valor:,.2f} efetuado com sucesso\n")
		
	def transferir(self, origem_login, destino_login, valor):
	  cliente_origem = self.banco.buscar_usuario(origem_login)
	  cliente_destino = self.banco.buscar_usuario(destino_login)
	  if cliente_origem is None or cliente_destino is None:
	    print("Usuário não existe ou não encontrado")
	    return
	  if valor <= 0:
	    print("Valor incorreto.")
	    return 
	  if cliente_origem.saldo < valor:
	    print("Saldo insuficiente para a transaçao")
	    return
	  cliente_origem.saldo -= valor
	  cliente_destino.saldo += valor
	  print(f"Transferência de {cliente_origem.nome} para {cliente_destino.nome} realizado com sucesso")
	  print(f"Novo saldo atual de {cliente_origem.nome}, R$ {cliente_origem.saldo}.")
	  print(f"Novo saldo atual de {cliente_destino.nome} R$ {cliente_destino.saldo}.")
		  
class Usuarios:
	def __init__(self, nome, login, saldo):
		self.nome=nome
		self.login=login
		self.saldo=saldo
		
	def exibir(self):
		print(f"O usuário encontrado foi o {self.nome}, o login cadastrado é {self.login}, o saldo da conta atual é de R${self.saldo:,.2f}\n")

banco=Banco()
usuario1=Usuarios("Daniel", "dan123", 100)
usuario2=Usuarios("Elizete", "eli133", 500)
usuario3=Usuarios("Daniele", "nyele128", 600)
	
banco.adicionar_usuarios(usuario1)
banco.adicionar_usuarios(usuario2)
banco.adicionar_usuarios(usuario3)

u=banco.buscar_usuario("nyele128")
if u:
	u.exibir()
else:
	print("Usuário não encontrado")
	
	
service=ContaService(banco)
service.depositar("nyele128", 400)

#u.exibir()

a=banco.buscar_usuario("dan123")
service.sacar("dan123", 100)

#a.exibir()

service.transferir("nyele128", "dan123", 500)
#a.exibir()