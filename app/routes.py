from flask import current_app as app # Importa o app que está rodando
from flask import render_template, jsonify
from .models import Veiculo
from flask_login import LoginManager
from wtforms import validators


#login_manager = LoginManager()

@app.route('/') # o símbolo "@" significa "Decorador" - Basicamente está dizendo: "Flask, fique de olho na porta principal (/). Se alguém entrar, execute a função abaixo."
def index():
    return render_template('index.html')

@app.route('/veiculos')
def listar_veiculos():

    # Buscamos todos os veículos do banco de dado
    lista_de_veiculos = Veiculo.query.all()

    # Passamos a lista para o HTML através da variável 'veiculos'
    return render_template('ConsultaDeVeiculos.html', veiculos = lista_de_veiculos)

@app.route('/api/veiculo/<string:placa>')
def api_detalhe_veiculo(placa):
    veiculo = Veiculo.query.get_or_404(placa)
    dados = {
        "placa": veiculo.placa,
        "modelo": veiculo.modelo,
        "marca": veiculo.marca,
        "ano": veiculo.ano,
        "combustivel": veiculo.combustivel.value,
        "Km_atual": veiculo.Km_Atual,
        "Km_UltimaTrocaOleo": veiculo.Km_UltimaTrocaOleo,
        "Km_UltimaRevisao": veiculo.Km_UltimaRevisao,
        "Data_ultimaRevisao": veiculo.Data_ultimaRevisao.strftime('%d/%m/%Y'),
        "status": veiculo.status.value
    }
    return jsonify(dados)

@app.route('/login', methods=['POST'])
def login_user():
