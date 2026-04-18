class ContaService:
  def __init__(self, repo):
    self.repo = repo
    
  def cadastrar(self, nome, login, senha):
    usuario = self.repo.buscar_por_login(login)
    if usuario:
      return{"msg": "Usuario já cadastrado"}
      
    from usuario import Usuarios
    novo = Usuarios(nome, login, senha)
    
    self.repo.cadastrar(novo)
    return{"msg": "Cadastro efetuado com sucesso!"}
    
  def login(self, login, senha):
    usuario = self.repo.buscar_por_login(login)
    
    if usuario is None:
        return {"Erro": "Usuário não encontrado!"}
    if senha != usuario.senha:
      return {"Erro": "Usuário ou senha inválido!"}
    
    return {"msg": f"Seja bem-vindo {usuario.nome}!")
    