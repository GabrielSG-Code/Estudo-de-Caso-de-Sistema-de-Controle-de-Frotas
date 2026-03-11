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

class TipoCombustivel(enum.Enum):
    GASOLINA = "Gasolina"
    ETANOL = "Etanol"
    DIESEL = "Diesel"
    GNV = "GNV"

class CategoriaCNH(enum.Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    AB = "AB"
    AC = "AC"
    AD = "AD"
    AE = "AE"

class StatusMotorista(enum.Enum):
    ATIVO = 'Ativo'
    INATIVO = 'Inativo'
    EM_VIAGEM = 'Em Viagem'
    FERIAS = 'Férias'
    AFASTADO = 'Afastado/Licença'

class StatusPneu(enum.Enum):
    NOVO = 'Novo'
    MEIO = 'Meio de Vida/Uso'
    VELHO = 'Velho/Usado'

class PrioridadeOrdemServico(enum.Enum):
    EMERGENCIAL = 'Emergencial/Critica' #Parada Imediata
    ALTA = 'Alta' #Risco de Segurança
    MEDIA = "Média" #Manutenção Programada Necessária
    BAIXA = 'Baixa' #Preventiva Agendada e/ou Estética

class TipoManutencao(enum.Enum):
    PREVENTIVA = 'Preventiva'
    CORRETIVA = 'Corretiva'
    PREDITIVA = 'Preditiva'

class EstadoEmpresa(enum.Enum):
    SP = 'São Paulo'
    BA = 'Bahia'


# Classes de Orientação a Objeto
#### SISTEMA #####
class Usuario(db.Model):
    __tablename__ = 'usuarios'

    usuario_id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100), nullable = False, index = True)
    cpf = db.Column(db.String(11), unique = True, index = True, nullable = False)
    telefone = db.Column(db.String(11), unique = True, nullable = False)
    email = db.Column(db.String(100), nullable = False, unique = True)
    senha = db.Column(db.String(255), nullable = False)

    # Nível de Acesso: 1-Super Admin; 2-Admin; 3-Usuário

    nivel_acesso = db.Column(db.Integer, default=3)
    veiculos = db.relationship('Veiculo', backref='proprietario', lazy = True)

class Empresa(db.Model):

    __tablename__ = 'empresas'

    id_empresa = db.Column(db.Integer, primary_key = True, nullable = False)
    nome = db.Column(db.String(200), nullable = False)
    cnpj = db.Column(db.String(14), nullable = False, index = True, unique = True)
    estado = db.Column(db.Enum(EstadoEmpresa), index = True, nullable = False)
    endereco = db.Column(db.String(200), nullable = False)
    proprietario = db.Column(db.String(100), nullable = False)

    #RELACIONAMENTOS

    veiculos = db.relationship('Veiculo', backref = 'empresa', lazy = True)



#### INFORMAÇÕES SOBRE A FROTA ####

class Veiculo(db.Model):
    __tablename__ = 'veiculos'

    placa = db.Column(db.String(7), primary_key = True, index = True)
    modelo = db.Column(db.String (50), nullable = False, index = True)
    marca = db.Column(db.String(100), nullable = False, index = True)
    ano = db.Column(db.Integer, nullable = False, index = True)
    tipo_veiculo = db.Column(db.String(100), nullable = False, index = True)
    combustivel = db.Column(db.Enum(TipoCombustivel), nullable = False)
    km_atual = db.Column(db.Float, nullable = False)
    km_ultima_troca_oleo = db.Column(db.Float, nullable = False)
    km_ultima_revisao = db.Column(db.Float, nullable = False)
    data_ultima_revisao = db.Column (db.DateTime, default = lambda: datetime.now(timezone.utc), nullable = False)
    data_ultima_atualizacao = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc), onupdate= lambda: datetime.now(timezone.utc), nullable = False)
    status_veiculo = db.Column(db.Enum(StatusVeiculo), default = StatusVeiculo.ATIVO, nullable = False, index = True)

    # CHAVE ESTRANGEIRA: Liga o veículo ao usuário que o cadastrou

    id_veiculo_criado_por = db.Column(db.Integer, db.ForeignKey('usuarios.usuario_id'), nullable = False, index = True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id_empresa'), nullable = False, index = True)

    # RELACIONAMENTOS

    viagens = db.relationship('Viagem', backref = 'veiculo', lazy = True)
    abastecimentos = db.relationship('Abastecimento', backref = 'veiculo', lazy = True) 
    ordem_servicos = db.relationship('OrdemServico', backref = 'veiculo', lazy = True)
    manutencoes = db.relationship('Manutencao', backref = 'veiculo', lazy = True)

class Motorista(db.Model):

    __tablename__ = 'motoristas'
    motorista_id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100), nullable = False, index = True)
    CPF = db.Column(db.String(11), unique = True, index = True, nullable = False)
    telefone = db.Column(db.String(11), unique = True, nullable = False)
    CNH = db.Column(db.Enum(CategoriaCNH), default = CategoriaCNH.B, nullable = False, index = True)
    validade_cnh = db.Column(db.Date)
    status_motorista = db.Column(db.Enum(StatusMotorista), default = StatusMotorista.ATIVO, nullable = False, index = True)

class Pneu(db.Model):

    __tablename__='pneus'

    id_pneu = db.Column(db.Integer, primary_key = True)
    data_instalacao = db.Column(db.Date, nullable = False)
    km_instalacao = db.Column(db.Float, nullable = False)
    km_atual = db.Column(db.Float, nullable = False)
    vida_util_km = db.Column(db.Float, nullable = False)
    status_pneu = db.Column(db.Enum(StatusPneu), default = StatusPneu.NOVO, nullable = False, index = True)
    custo = db.Column(db.Numeric(10,2), nullable = False)

    #Chave Estrangeira

    veiculo_pertencente = db.Column(db.String(7), db.ForeignKey('veiculos.placa'), nullable=False, index=True)


#### SERVIÇOS ####


class OrdemServico (db.Model):

    __tablename__ = 'ordem_servicos'

    id_ordem_servico = db.Column (db.Integer, unique = True, nullable = False, primary_key = True)
    data_abertura = db.Column(db.Date, nullable = False)
    tipo_servico = db.Column (db.String(100), nullable = False)
    descricao_problema = db.Column(db.String(500), nullable = False)
    prioridade = db.Column(db.Enum(PrioridadeOrdemServico), default = PrioridadeOrdemServico.ALTA, nullable = False, index = True)
    data_conclusao = db.Column(db.Date)
    custo_total = db.Column(db.Numeric(10,2))

    #CHAVE ESTRANGEIRA

    veiculo_placa = db.Column (db.String(7), db.ForeignKey('veiculos.placa'), nullable = False, index = True)

class Manutencao(db.Model):

    __tablename__ = 'manutencoes'

    id_manutencao = db.Column(db.Integer, unique = True, nullable = False, primary_key = True)
    tipo = db.Column(db.Enum(TipoManutencao), nullable = False, index = True)
    descricao = db.Column (db.String(500), nullable = False)
    data = db.Column(db.Date, nullable = False)
    km_veiculo = db.Column (db.Float, nullable = False)
    custo = db.Column(db.Numeric(10,2), nullable = False)
    fornecedor = db.Column (db.String(100), nullable = False)

    #CHAVE ESTRANGEIRA

    veiculo_placa = db.Column (db.String(7), db.ForeignKey('veiculos.placa'), nullable = False, index = True)

class Abastecimento(db.Model):
    
    __tablename__ = 'abastecimentos'

    id_abastecimento = db.Column(db.Integer, unique = True, nullable = False, primary_key = True)
    data = db.Column (db.Date, nullable = False)
    km_veiculo = db.Column (db.Float, nullable = False)
    litros = db.Column (db.Float , nullable = False)
    valor_total = db.Column (db.Numeric(10,2), nullable = False)
    valor_por_litro = db.Column(db.Numeric(10,2), Computed("valor_total / litros"), nullable = False)
    posto = db.Column(db.String(100), nullable = False, index = True)

    #CHAVE ESTRANGEIRA

    veiculo_placa = db.Column(db.String(7), db.ForeignKey('veiculos.placa'), nullable = False, index = True)


#### VIAGEM ####

class Viagem(db.Model):

    __tablename__ = 'viagens'

    id_viagem = db.Column(db.Integer, primary_key = True)
    data_saida = db.Column(db.Date, nullable = False)
    km_saida = db.Column(db.Float, nullable = False)
    data_retorno = db.Column(db.Date)
    km_retorno = db.Column(db.Float)

    #CHAVES ESTRANGEIRAS

    motorista_cadastrado = db.Column(db.Integer, db.ForeignKey('motoristas.motorista_id'), nullable = False, index = True)
    veiculo_cadastrado = db.Column(db.String(7), db.ForeignKey('veiculos.placa'), nullable = False, index = True)