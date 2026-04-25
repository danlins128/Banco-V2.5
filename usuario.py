class Usuarios:
    def __init__(self, nome, sobrenome, email, login, senha, saldo=0, conta=0):
        self.nome = nome
        self.sobrenome = sobrenome
        self.email = email
        self.login = login
        self.senha = senha
        self.saldo = saldo
        self.conta = conta