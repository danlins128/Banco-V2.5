from flask import Flask, request, jsonify
from repository import UsuarioRepository
from usuario import Usuarios
from service import ContaService

app = Flask(__name__)
repo = UsuarioRepository()
service= ContaService(repo)

@app.route("/")
def home():
    return "Servidor Rodando"
    
@app.route("/cadastrar", methods=["POST"])
def cadastro():
    data = request.json
    nome = data.get("nome")
    login = data.get("login")
    senha = data.get("senha")
    return service.cadastrar(nome, login, senha)
    
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    login = data.get("login")
    senha = data.get("senha")
    return service.login(login,senha)
    
    
if __name__ == "__main__":
    app.run(debug=True)
