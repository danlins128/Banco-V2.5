class ContaService:
  def __init__(self, repo):
    self.repo = repo
    
  def cadastrar(self, nome, sobrenome, email, login, senha):
    
    if self.repo.buscar_por_login(login):
      return{"erro": "Usuario já cadastrado"}
    
    if self.repo.buscar_por_email(email):
       return {'erro': "E-mail já utilizado"}
    
    from usuario import Usuarios

    novo = Usuarios(nome, sobrenome, email, login, senha)

    self.repo.cadastrar(novo)
    return{"msg": "Cadastro efetuado com sucesso!"}
    
  def login(self, login, senha):
    usuario = self.repo.buscar_por_login(login)
    
    if usuario is None:
        return {"erro": "Usuário não encontrado!"}
    if senha != usuario.senha:
        return {"erro": "Usuário ou senha inválido!"}
    
    return {
      "nome":usuario.nome,
      "conta":usuario.conta,
      "saldo":usuario.saldo
    }

  def saldo(self, conta):
     return self.repo.busca_saldo(conta)
  
  def depositar(self, conta, valor):
     valor_atual = self.repo.busca_saldo(conta)
     valor += valor_atual
     self.repo.atualizar_saldo(conta, valor)
     return valor
  
  def sacar(self,conta ,valor):
    valor_atual = self.repo.busca_saldo(conta)
    if valor > valor_atual:
      return {"erro": "Saldo insuficiente!", "valor": valor_atual}
    valor_atual -= valor
    self.repo.atualizar_saldo(conta, valor_atual)
    return valor_atual