from flask import Flask, request, session, redirect, url_for, render_template
from repository import UsuarioRepository
from service import ContaService

app = Flask(__name__)
app.secret_key = "Secret_Key"
repo = UsuarioRepository()
service= ContaService(repo)

@app.route("/")
def home():
    return render_template("index.html")
    
@app.route("/cadastrar", methods=["GET", "POST"])
def cadastro():
  if request.method=="GET":
    return render_template("cadastrar.html")
  data = request.form
  nome = data.get("nome")
  login = data.get("login")
  senha = data.get("senha")
  resultado = service.cadastrar(nome, login, senha)
  if "erro" in resultado:
    return render_template("index.html", mensagem_erro=resultado["erro"])
  if "msg" in resultado:
    return render_template("index.html", mensagem_sucesso=resultado["msg"])
    
@app.route("/login", methods=["POST"])
def login():
    data = request.form #1 pega os dados
    resultado = service.login(
        data.get("login"),
        data.get("senha")
    )#2 usa o service.py
    if "erro" in resultado:
        return render_template("index.html", mensagem_erro=resultado["erro"]) #3 não cria sessão, deu erro.
    session["conta"] = resultado["conta"]
    session["nome"] = resultado["nome"]
    #4 guarda quem está logado
    return redirect(url_for("menu")) # redireciona se login for efetuado
    
@app.route("/menu", methods=["GET"])
def menu():
  if "conta" not in session:
    return render_template("index.html")
  return render_template("menu.html")
  
@app.route("/logout")
def logout():
  session.clear()
  return redirect(url_for("home"))
    
@app.route("/saldo", methods=["GET"])
def ver_saldo():
    if "conta" not in session:
        return {"erro": "Usuário não logado"}
        
    saldo = repo.busca_saldo(session["conta"])
    return {"saldo":saldo}
    
    
if __name__ == "__main__":
    app.run(debug=True)
