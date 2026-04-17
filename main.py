from service import ContaService
from repository import UsuarioRepository

repo = UsuarioRepository()
service = ContaService()

service.cadastrar("Daniel", "danzinho", "dan123")