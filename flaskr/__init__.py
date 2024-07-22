"""
Em vez de criar uma instancia global do flask, fazemos isso dentro de uma funcao,
a "application factory", qualquer configuracao ou setup ocorrera dentro dessa
funcao e a aplicacao será retornada
"""

import os

from flask import Flask

from flaskr import auth


def create_app(test_config=None):
    """criacao e configuracao do app"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",  # TODO: alterar a chaves de enviar p/ prod
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # carrega a configuracao da instancia, caso exista, quando não estivermos testando
        app.config.from_pyfile("config.py", silent=True)
    else:
        # carrega as configuracoes de teste, se passadas
        app.config.from_mapping(test_config)

    # garante que o diretorio da instancia existe
    try:
        os.makedirs(app.instance_path)  # type: ignore
    except OSError:
        pass

    # uma pagina simples com hello world

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    from . import db

    app.register_blueprint(auth.bp)  # type: ignore
    # db.init_app(app)

    return app
