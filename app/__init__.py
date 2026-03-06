from flask import Flask
from .models import db
import os

def create_app():
    app = Flask(__name__)

    
    ## Isso descobre o caminho da pasta onde este arquivo __init__.py está
    basedir = os.path.abspath(os.path.dirname(__file__))

    ## Isso sobe um nível e entra na pasta 'instance', garantindo o caminho correto
    db_path = os.path.join(basedir, '..', 'instance', 'frota.db')

    # Configuração do Banco de Dados (SQLLite para começar, que cria um arquivo local)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all() # Isso cria o arquivo .db automaticamente baseado no models.py

        from . import routes # Importa as rotas para o contexto do app
    return app