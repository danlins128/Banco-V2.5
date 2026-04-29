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
    self.repo.depositar(conta, valor)
    return self.repo.busca_saldo(conta)
  
  def sacar(self, conta, valor):
    resultado = self.repo.sacar(conta, valor)    

    if resultado is None:
        return {"erro": "Saldo insuficiente!", "valor": self.repo.busca_saldo(conta)}

    return resultado
  
  def transferir(self, conta_local, conta_destino, valor):
    if not self.repo.buscar_por_conta(conta_destino):
        return {'erro': 'Usuário inexistente'}

    resultado = self.repo.transferir(conta_local, conta_destino, valor)

    if resultado is None:
        return {'erro': 'Saldo insuficiente!', 'valor': self.repo.busca_saldo(conta_local)}

    return {"msg": "Transferência realizada"}
  
  def extrato(self, conta):
    return self.repo.buscar_transacao(conta)
    