from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

@app.route("/")
def home():
    return "Servidor Rodando"
    
@app.route("/user/<nome>")
def user(nome):
    return f"Olá {nome}"
    
@app.route("/api")
def api():
    return jsonify({
    "nome": "Daniel",
    "status": "online"
    })
    
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    
    usuario = data.get("usuario")
    senha = data.get("senha")
    
    return jsonify ({
    "msg": f"Login recebido: {usuario}"
    })
    
if __name__ == "__main__":
    app.run(debug=True)
