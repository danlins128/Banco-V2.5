from service import ContaService
from repository import UsuarioRepository
import flask

repo = UsuarioRepository()
service = ContaService(repo)

#service.cadastrar("Daniel", "danlins", "dan123")
#service.cadastrar("Daniele", "nyele", "ny123")
#service.cadastrar("Daniel Danas", "dantasalves", "dantas123")
#service.login("danlins", "dan123")