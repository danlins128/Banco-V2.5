class Usuarios:
    def __init__(self, nome, login, senha, saldo=0, conta=0):
        self.nome = nome
        self.login = login
        self.senha = senha
        self.saldo = saldo
        self.conta = conta