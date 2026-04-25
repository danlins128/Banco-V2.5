from flask import Flask, request, session, redirect, url_for, render_template, make_response
from repository import UsuarioRepository
from service import ContaService

app = Flask(__name__)
app.secret_key = "Secret_Key"
repo = UsuarioRepository()
service= ContaService(repo)

@app.template_filter('dinheiro')
def format_dinheiro(valor):
  try:
   return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
  except (ValueError, TypeError):
    return "0.00"
    
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
    return render_template("cadastrar.html", mensagem_erro=resultado["erro"])
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
    session["saldo"] = resultado["saldo"]
    #4 guarda quem está logado
    return redirect(url_for("menu")) # redireciona se login for efetuado
    
@app.route("/menu", methods=["GET"])
def menu():
  if "conta" not in session:
    return render_template("index.html")
  return render_template("menu.html")
  
@app.route("/menu/deposito")
def menu_deposito():
  return render_template("/partials/deposito.html")

@app.route("/menu/saque", methods=["GET", "POST"])
def menu_saque():
    return render_template("/partials/saque.html")
  
@app.route("/logout")
def logout():
  session.clear()
  return redirect(url_for("home"))
    
@app.route("/saldo")
def ver_saldo():
    if "conta" not in session:
        return {"erro": "Usuário não logado"}
        
    saldo = service.saldo(session["conta"])
    session["saldo"] = saldo
    
    return render_template("partials/saldo.html")
@app.route("/deposito", methods=["POST"])
def deposito():
    if "conta" not in session:
        return {"erro": "Usuário sem permissão"}
    valor = request.form.get("valor")
    if valor == "":
        return {"erro": "Digite um valor válido no campo acima"}
    else:
        valor = float(valor)
        service.depositar(session["conta"], valor)
        response = make_response(render_template ("partials/deposito_sucesso.html", valor=valor))
        response.headers["HX-Trigger"]="atualizarSaldo"
        
        return response
    
@app.route("/saque", methods=["POST"])
def sacar():
    if "conta" not in session:
        return {"erro": "Usuário sem permissão"}
    valor = request.form.get("valor")
    if valor == "":
        return {"erro": "Digite um valor válido no campo acima"}
    else:
        valor = float(valor)
        resultado = service.sacar(session["conta"], valor)
        if isinstance(resultado, dict) and "erro" in resultado:
            return resultado
        response = make_response(render_template ("partials/saque_sucesso.html", valor=valor))
        response.headers["HX-Trigger"]="atualizarSaldo"
        
        return response

    
if __name__ == "__main__":
    app.run(debug=True)
