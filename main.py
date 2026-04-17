from service import ContaService
from repository import UsuarioRepository

repo = UsuarioRepository()
service = ContaService(repo)

#service.cadastrar("Daniel", "danlins", "dan123")
#service.cadastrar("Daniele", "nyele", "ny123")

