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