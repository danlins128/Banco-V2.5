class ContaService:
  def __init__(self, repo):
    self.repo = repo
    
  def cadastrar(self, nome, login, senha):
    usuario = self.repo.buscar_por_login(login)
    if usuario:
      return{"erro": "Usuario já cadastrado"}
    
    from usuario import Usuarios
    novo = Usuarios(nome, login, senha)
    if novo.nome is "" or novo.login is "" or novo.senha is "":
        return{"erro": "Preencha todos os campos"}


    self.repo.cadastrar(novo)
    return{"msg": "Cadastro efetuado com sucesso!"}
    
  def login(self, login, senha):
    if not login or not senha:
        return {"erro": "Preencha todos os campos"}
    
    usuario = self.repo.buscar_por_login(login)
    
    if usuario is None:
        return {"erro": "Usuário não encontrado!"}
    if senha != usuario.senha:
      return {"erro": "Usuário ou senha inválido!"}
    
    return {
      "success": True,
      "nome":usuario.nome,
      "conta":usuario.conta,
    }

  def atualizar_saldo(self, conta):
    saldo_atual = self.repo.busca_saldo(conta)
    if saldo_atual is not None:
        self.repo.atualizar_saldo(conta, saldo_atual)
        return {"msg": "Saldo atualizado com sucesso!"}
    return {"erro": "Conta não encontrada!"}