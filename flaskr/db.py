"""arquivo com a conexão a db"""

from mimetypes import init
import sqlite3

import click
from flask import current_app, g


def get_db():
    # g é um objeto especial, unico para cada requisicao
    # é utilizado para guardar dados que possam ser acessados por multiplas
    # funcoes durante a requisicao. A conexao é armazeanda e reusada em vez
    # de recriada caso get_db seja chamada novamente em uma mesma requisicao
    if "db" not in g:

        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        """
        current app é um objeto especial que aponta para o app Flask lidando com a
        requisicao.
        """
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        """
        open_resource() -> abre um arquivo relativo ao
        pacote(diretorio) flaskr (util pois nao necessaria-
        mente sabemos dessa localizacao ao fazer o deploy do app )
        """
        db.executescript(f.read().decode("utf8"))


"""
click.command() -> comando da cli chamando "init-db" que chama
a funcao "init_db" e exibe uma mensagem para o usuário
"""


@click.command("init-db")
def init_db_command():
    """limpa os dados existentes e cria novas tabelas"""

    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """
    as funcoes close_db e init_db_command devem estar registradas
    na instancia do app, senao, nao serao usadas pela aplicacao.
    Porém, como estamos usando uma funcao factory, a instancia não
    está disponivel quando escrevemos as funcoes. Entao, escrevemos
    uma funcao que recebe uma aplicacao e faz o registro
    """
    app.teardown_appcontext(close_db)
    """
    diz ao Flask para chamas esta funcao quando estivar fazendo
    o clean-up depois de retornar uma resposa
    """
    app.cli.add_command(init_db_command)
    """
    adicionada um novo comando que pode ser chamado com os
    comandos flask
    """
