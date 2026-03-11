from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Computed
from datetime import datetime, timezone
import enum

db = SQLAlchemy()

#Listas Pré-configuradas para Preenchimento
class StatusVeiculo(enum.Enum):
    ATIVO = "Ativo"
    MANUTENCAO = "Manutenção"
    VENDIDO = "Vendido"
    INATIVO = "Inativo"

class TipoCombustível(enum.Enum):
    GASOLINA = "Gasolina"
    ETANOL = "Etanol"
    DIESEL = "Diesel"
    GNV = "GNV"


# Classes de Orientação a Objeto
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False, unique = True)
    senha = db.Column(db.String(255), nullable = False, unique = True)

    # Nível de Acesso: 1-Super Admin; 2-Admin; 3-Usuário

    nivel_acesso = db.relationship('Veiculo', backref='proprietario', lazy = True)

class Veiculo(db.Model):
    __tablename__ = 'veiculos'
    placa = db.Column(db.String(7), primary_key = True)
    modelo = db.Column(db.String (50), nullable = False)
    marca = db.Column(db.String(100), nullable = False)
    ano = db.Column(db.Integer, nullable = False)
    tipoVeiculo = db.Column(db.String(100), nullable = False)
    combustivel = db.Column(db.Enum(TipoCombustível), nullable = False)
    Km_Atual = db.Column(db.Float, nullable = False)
    Km_UltimaTrocaOleo = db.Column(db.Float, nullable = False)
    Km_UltimaRevisao = db.Column(db.Float, nullable = False)
    Data_ultimaRevisao = db.Column (db.Date, default = datetime.utcnow, nullable = False)
    Data_ultimaAtualizacao = db.Column(db.DateTime, onupdate=datetime.utcnow, nullable = False)
    status = db.Column(db.Enum(StatusVeiculo), default = StatusVeiculo.ATIVO, nullable = False)

    # CHAVE ESTRANGEIRA: Liga o veículo ao usuário que o cadastrou

    id_usuarioCriado = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

