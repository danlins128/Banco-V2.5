from werkzeug.security import generate_password_hash, check_password_hash

class ContaService:
  def __init__(self, repo):
    self.repo = repo
    
  def cadastrar(self, nome, sobrenome, email, login, senha):
    
    if self.repo.buscar_por_login(login):
      return{"erro": "Usuario já cadastrado"}
    
    if self.repo.buscar_por_email(email):
       return {'erro': "E-mail já utilizado"}
    
    from usuario import Usuarios

    senha_hash = generate_password_hash(senha)

    novo = Usuarios(nome, sobrenome, email, login, senha_hash)

    self.repo.cadastrar(novo)
    return{"msg": "Cadastro efetuado com sucesso!"}
    
  def login(self, login, senha):
    usuario = self.repo.buscar_por_login(login)
    
    if usuario is None:
        return {"erro": "Usuário não encontrado!"}
    if not check_password_hash(usuario.senha , senha):
        return {"erro": "Usuário ou senha inválido!"}
    
    return {
      "nome":usuario.nome,
      "sobrenome":usuario.sobrenome,
      "conta":usuario.conta,
      "saldo":usuario.saldo
    }

  def saldo(self, conta):
     return self.repo.busca_saldo(conta)
  
  def depositar(self, conta, valor):
     saldo_atual = self.repo.busca_saldo(conta)
     novo_saldo = saldo_atual + valor
     self.repo.atualizar_saldo(conta, novo_saldo)
     self.repo.registrar_transacao(conta, None, "deposito", valor)
     return novo_saldo
  
  def sacar(self,conta ,valor):
    valor_atual = self.repo.busca_saldo(conta)
    if valor > valor_atual:
      return {"erro": "Saldo insuficiente!", "valor": valor_atual}
    valor_atual -= valor
    self.repo.atualizar_saldo(conta, valor_atual)
    self.repo.registrar_transacao(conta, None, "saque", valor)
    return valor_atual
  
  def transferir(self, conta_local, conta_destino, valor):
    usuario_destino = self.repo.buscar_por_conta(conta_destino)  
    if usuario_destino is None:
       return {'erro': 'Usuário inexistente'}
      
    saldo_origem = self.repo.busca_saldo(conta_local)
    saldo_destino = self.repo.busca_saldo(conta_destino)

    if valor > saldo_origem:
       return {'erro': 'Saldo insuficiente!', "valor": saldo_origem}
    
    debitancia = saldo_origem - valor
    transferencia =  saldo_destino + valor

    self.repo.atualizar_saldo(conta_local, debitancia)
    self.repo.atualizar_saldo(usuario_destino.conta, transferencia)
    self.repo.registrar_transacao(conta_local, conta_destino, "transferencia", valor)

    return valor
  
  def extrato(self, conta):
    return self.repo.buscar_transacao(conta)
    