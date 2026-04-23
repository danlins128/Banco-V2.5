from flask import Flask, request, session, redirect, url_for, render_template, jsonify
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
    data = request.get_json() #1 pega os dados
    resultado = service.login( #2 usa o service.py
        data.get("login"),
        data.get("senha")
    )
    if "erro" in resultado: #3 se tiver erro, retorna o erro
      return jsonify({
            "success": False,
            "message": resultado["erro"]
        })
    session["conta"] = resultado["conta"]
    session["nome"] = resultado["nome"]
        #4 guarda quem está logado
    return jsonify({"success": True}) # redireciona se login for efetuado
    
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
    return render_template("/saque.html")
  
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
    
@app.route("/depositar", methods=["POST"]) # Rota para realizar depósito
def depositar():
    if "conta" not in session:
        return {"erro": "Usuário não logado"}
    
    data = request.get_json() # pega os dados
    valor = data.get("valor") # pega o valor do depósito
    
    if valor is None or valor <= 0: # verifica se o valor é válido
        return {"erro": "Valor inválido"}
    
    # Lógica para atualizar o saldo do usuário no banco de dados
    # Exemplo: repo.depositar(session["conta"], valor)
    
    return {"success": True, "message": f"Depósito de R$ {valor:.2f} realizado com sucesso!"}


if __name__ == "__main__":
    app.run(debug=True)
