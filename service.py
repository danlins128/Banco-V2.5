class ContaService:
  def __init__(self, repo):
    self.repo = repo
    
  def cadastrar(self, nome, login, senha):
    usuario = self.repo.buscar_por_login(login)
    if usuario:
      print("Usuario já cadastrado")
      return
    from usuario import Usuario
    novo = Usuario(nome, login, senha)
    
    self.repo.cadastrar(novo)
    print("Cadastro efetuado com sucesso!")
    
  def login(self, login, senha):
    usuario = self.repo.buscar_por_login(login)
    
    if usuario is None:
      print("Usuário não encontrado!")
      return
    if senha != usuario.senha:
      print("Usuário ou senha inválido!")
      return
    
    print(f"Seja bem-vindo {usuario.nome}!")
    return usuario