class ContaService:
  def __init__(self, repo):
    self.repo = repo
    
  def cadastrar(self, nome, sobrenome, email, login, senha):
    usuario = self.repo.buscar_por_login(email, login)
    if usuario:
      return{"erro": "Usuario já cadastrado"}
    
    from usuario import Usuarios
    novo = Usuarios(nome, sobrenome, email, login, senha)
    if novo.nome == "" or novo.login == "" or novo.senha == "":
        return{"erro": "Preencha todos os campos"}

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
      return {"erro": "Saldo insuficiente!"}
    valor_atual -= valor
    self.repo.atualizar_saldo(conta, valor_atual)
    return valor_atual