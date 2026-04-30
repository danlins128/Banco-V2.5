# 💸 Daniel's Bank

Sistema bancário web desenvolvido com Flask, com arquitetura real em cloud utilizando AWS.

---

## Demonstração

https://danielsbank.duckdns.org

---

##  Sobre o projeto

Aplicação web que simula operações bancárias básicas:

* Cadastro de usuários
* Login com autenticação segura
* Depósitos
* Saques
* Transferências entre contas
* Extrato de transações

O foco do projeto vai além do código: foi construído com uma arquitetura próxima de produção, incluindo deploy em nuvem e configuração de infraestrutura.

---

## ⚙️ Tecnologias utilizadas

### Backend

* Python
* Flask
* Gunicorn

### Banco de Dados

* PostgreSQL
* AWS RDS

### Infraestrutura

* AWS EC2
* Nginx (proxy reverso)
* systemd (gerenciamento de processo)
* Let's Encrypt (HTTPS)

---

## 🔐 Segurança

* Senhas armazenadas com hash (`werkzeug.security`)
* Conexão segura via HTTPS
* Porta 8000 protegida (acesso apenas interno para teste quando necessário)
* Proxy reverso com Nginx

---

## ☁️ Deploy

A aplicação foi deployada manualmente em uma instância EC2, incluindo:

* Configuração de Security Groups
* Acesso via SSH
* Configuração do Nginx
* Integração com RDS
* Criação de serviço com systemd
* Certificado SSL com Certbot
* DNS gerado gratuitamente no duckdns.org

---

## 🧪 Como rodar localmente

```bash
# Clonar o projeto
git clone https://github.com/danlins128/Banco-V2.5.git

cd "na pasta do projeto"

# Criar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variável de ambiente
export DATABASE_URL="postgresql://usuario:senha@localhost:5432/sistema_bancario"

# Rodar aplicação
python app.py
```

---

## 📌 Próximos passos

* Containerização com Docker
* CI/CD automatizado
* Monitoramento da aplicação

---

## 👨‍💻 powered by: Daniel Lins

Projeto focado em aprendizado prático de backend + cloud + DevOps.
