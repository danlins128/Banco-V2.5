from flask import Flask, request, session
from repository import UsuarioRepository
from service import ContaService

app = Flask(__name__)
app.secret_key = "Secret_Key"
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
    data = request.json #1 pega os dados
    resultado = service.login(
        data.get("login"),
        data.get("senha")
    )#2 usa o service.py
    if "erro" in resultado:
        return resultado #3 não cria sessão, deu erro.
    session["conta"] = resultado["conta"]
    #4 guarda quem está logado
    return {"msg":"Sessão iniciada com sucesso!"}
    
if __name__ == "__main__":
    app.run(debug=True)
