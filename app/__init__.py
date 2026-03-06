from flask import Flask
from .models import db

def create_app():
    app = Flask(__name__)

    # Configuração do Banco de Dados (SQLLite para começar, que cria um arquivo local)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///frota.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all() # Isso cria o arquivo .db automaticamente baseado no models.py

        from . import routes # Importa as rotas para o contexto do app
    return app