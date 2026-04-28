from flask import Flask, flash, request, session, redirect, url_for, render_template, make_response
from repository import UsuarioRepository
from service import ContaService
from forms import CadastroForm, LoginForm, TransferForm

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
       session["sobrenome"] = resultado["sobrenome"]
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
     
     flash('Usuário cadastrado com sucesso!', 'sucesso')
     return redirect(url_for('home'))
     
  return render_template("cadastrar.html", form=form)

  
@app.route("/menu", methods=["GET"])
def menu():
  if "conta" not in session:
    flash('Usuário não conectado!', 'erro')
    return redirect(url_for('home'))
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
        flash('Usuário não conectado!', 'erro')
        return redirect(url_for('home'))
        
    saldo = service.saldo(session["conta"])
    session["saldo"] = saldo
    
    return render_template("partials/saldo.html")

@app.route("/deposito", methods=["POST", 'GET'])
def deposito():
    if "conta" not in session:
        flash('Usuário não conectado!', 'erro')
        return redirect(url_for('home'))
    valor = request.form.get("valor")
    if valor == "":
        return {"erro": "Digite um valor válido no campo acima"}
    
    valor = float(valor)
    service.depositar(session["conta"], valor)
    response = make_response(render_template ("partials/deposito_sucesso.html", valor=valor))
    response.headers["HX-Trigger"]="atualizarSaldo"
        
    return response
    
@app.route("/saque", methods=["POST", "GET"])
def sacar():
    if "conta" not in session:
        flash('Usuário não conectado!', 'erro')
        return redirect(url_for('home'))
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

@app.route('/transferir', methods=["GET", "POST"])
def transferir():  
   
   if "conta" not in session:
      flash('Usuário não conectado!', 'erro')
      return redirect(url_for('home'))
   
   form = TransferForm()
   if form.validate_on_submit():
      resultado = service.transferir(
         session["conta"],
         form.conta_destino.data,
         form.valor.data
      )
      if isinstance(resultado, dict) and "erro" in resultado:
        return render_template('partials/transferencia_falha.html', erro = resultado['erro'], valor = session['saldo'])
      else:
        return render_template("partials/transferencia_sucesso.html", valor=form.valor.data)
      
   return render_template('transferencia.html', form=form)

@app.route('/menu/extrato')
def extrato():
    if "conta" not in session:
        flash('Usuário não conectado!', 'erro')
        return redirect(url_for('home'))
    transacoes = service.extrato(session["conta"])
    return render_template("partials/extrato.html", transacoes=transacoes, conta_logada=session['conta'])

if __name__ == "__main__":
    app.run(debug=True, port=8080)
