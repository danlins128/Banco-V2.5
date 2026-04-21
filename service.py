class ContaService:
  def __init__(self, repo):
    self.repo = repo
    
  def cadastrar(self, nome, login, senha):
    usuario = self.repo.buscar_por_login(login)
    if usuario:
      return{"erro": "Usuario já cadastrado"}
      
    from usuario import Usuarios
    novo = Usuarios(nome, login, senha)
    
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
     pass