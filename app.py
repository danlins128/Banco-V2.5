from flask import Flask, flash, request, session, redirect, url_for, render_template, make_response
from repository import UsuarioRepository
from service import ContaService
from forms import CadastroForm, LoginForm

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
    
@app.route("/", methods=['GET', 'POST'])
def home():
    form = LoginForm()
    
    
    # Quando o usuário entra no site, o método é GET (ele ignora esse if)
    # Quando ele clica em "Enviar", o método é POST e o if é validado
    if form.validate_on_submit():
       resultado = service.login(
          form.login.data,
          form.senha.data
       )
    
       if "erro" in resultado:
            return render_template("index.html", form=form, menssagem_erro=resultado["erro"]) #3 não cria sessão, deu erro.
       session["conta"] = resultado["conta"]
       session["nome"] = resultado["nome"]
       session["saldo"] = resultado["saldo"]
        #4 guarda quem está logado
       return redirect(url_for("menu"))

    return render_template('index.html', form=form)
       
@app.route("/cadastrar", methods=["GET", "POST"])
def cadastro():
  form = CadastroForm()

  if form.validate_on_submit():
     resultado = service.cadastrar(
        form.nome.data,
        form.sobrenome.data,
        form.email.data,
        form.login.data,
        form.senha.data
     )
     if "erro" in resultado:
        return render_template("cadastrar.html", form=form, menssagem_erro=resultado["erro"])
     
     return redirect(url_for('home'))
     
  return render_template("cadastrar.html", form=form)

  
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
            return render_template('partials/saque_falha.html', erro = resultado['erro'], valor = resultado['valor'])
        response = make_response(render_template ("partials/saque_sucesso.html", valor=valor))
        response.headers["HX-Trigger"]="atualizarSaldo"
        
        return response

    
if __name__ == "__main__":
    app.run(debug=True)
