import psycopg
import os
from random import randint
from usuario import Usuarios


class UsuarioRepository:

    def conectar(self):     
        return psycopg.connect(os.getenv("DATABASE_URL"))

    def _buscar_usuario(self, query, params):
        with self.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""SELECT nome, sobrenome, email, login, senha, saldo, conta 
                        FROM usuarios WHERE {query}""",
                    params
                )
                dados = cursor.fetchone()
                return Usuarios(*dados) if dados else None

    def buscar_por_login(self, login):
        return self._buscar_usuario("login = %s", (login,))

    def buscar_por_email(self, email):
        return self._buscar_usuario("email = %s", (email,))

    def buscar_por_conta(self, conta):
        return self._buscar_usuario("conta = %s", (conta,))

    def cadastrar(self, usuario):
        with self.conectar() as conn:
            with conn.cursor() as cursor:
                while True:
                    gerar_conta = randint(1000, 9999)

                    cursor.execute(
                        "SELECT 1 FROM usuarios WHERE conta = %s",
                        (gerar_conta,)
                    )

                    if not cursor.fetchone():
                        cursor.execute(
                            """INSERT INTO usuarios
                            (conta, nome, sobrenome, email, login, senha, saldo)
                            VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                            (
                                gerar_conta,
                                usuario.nome,
                                usuario.sobrenome,
                                usuario.email,
                                usuario.login,
                                usuario.senha,
                                usuario.saldo
                            )
                        )
                        break

    def busca_saldo(self, conta):
        with self.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT saldo FROM usuarios WHERE conta = %s",
                    (conta,)
                )
                resultado = cursor.fetchone()
                return resultado[0] if resultado else 0

    def atualizar_saldo(self, conta, valor):
        with self.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE usuarios SET saldo = %s WHERE conta = %s",
                    (valor, conta)
                )

    def registrar_transacao(self, conta_origem, conta_destino, tipo, valor):
        with self.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO transacoes 
                    (conta_origem, conta_destino, tipo, valor)
                    VALUES (%s, %s, %s, %s)""",
                    (conta_origem, conta_destino, tipo, valor)
                )

    def buscar_transacao(self, conta, limit=3):
        with self.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """SELECT conta_origem, conta_destino, tipo, valor, data_hora
                    FROM transacoes
                    WHERE conta_origem = %s OR conta_destino = %s
                    ORDER BY data_hora DESC
                    LIMIT %s""",
                    (conta, conta, limit)
                )
                return cursor.fetchall()

    def depositar(self, conta, valor):
        with self.conectar() as conn:
            with conn.cursor() as cursor:

                cursor.execute(
                "UPDATE usuarios SET saldo = saldo + %s WHERE conta = %s",
                (valor, conta)            )

                cursor.execute(
                """INSERT INTO transacoes 
                (conta_origem, conta_destino, tipo, valor)
                VALUES (%s, %s, %s, %s)""",
                (conta, None, "deposito", valor)            )

    def sacar(self, conta, valor):
        with self.conectar() as conn:
            with conn.cursor() as cursor:

                cursor.execute(
                "SELECT saldo FROM usuarios WHERE conta = %s FOR UPDATE",
                (conta,)
            )

                saldo = cursor.fetchone()[0]

                if valor > saldo:
                    return None

                cursor.execute(
                "UPDATE usuarios SET saldo = saldo - %s WHERE conta = %s",
                (valor, conta)
            )

                cursor.execute(
                """INSERT INTO transacoes 
                (conta_origem, conta_destino, tipo, valor)
                VALUES (%s, %s, %s, %s)""",
                (conta, None, "saque", valor)
            )

                return saldo - valor
        
    def transferir(self, conta_origem, conta_destino, valor):
        with self.conectar() as conn:
            with conn.cursor() as cursor:

            # trava origem
                cursor.execute(
                "SELECT saldo FROM usuarios WHERE conta = %s FOR UPDATE",
                (conta_origem,)
            )
                saldo_origem = cursor.fetchone()[0]

                if valor > saldo_origem:
                    return None

            # trava destino
                cursor.execute(
                "SELECT saldo FROM usuarios WHERE conta = %s FOR UPDATE",
                (conta_destino,)
            )

            # atualiza saldos
                cursor.execute(
                "UPDATE usuarios SET saldo = saldo - %s WHERE conta = %s",
                (valor, conta_origem)
            )

                cursor.execute(
                "UPDATE usuarios SET saldo = saldo + %s WHERE conta = %s",
                (valor, conta_destino)
            )

            # registra
                cursor.execute(
                """INSERT INTO transacoes 
                (conta_origem, conta_destino, tipo, valor)
                VALUES (%s, %s, %s, %s)""",
                (conta_origem, conta_destino, "transferencia", valor)
            )

            return True