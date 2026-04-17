class Usuarios:
    def __init__(self, nome, login, senha, saldo):
        self.nome = nome
        self.login = login
        self.senha = senha
        self.saldo = saldo
        self.conta = 0

    def exibir(self):
        print(f"O usuário encontrado foi o {self.				nome}, o login cadastrado é {self.login}, o 		saldo da conta atual é de R${self.saldo:,.				2f}\n")