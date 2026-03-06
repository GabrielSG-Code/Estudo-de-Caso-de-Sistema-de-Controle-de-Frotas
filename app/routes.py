from flask import current_app as app # Importa o app que está rodando
from flask import render_template
from .models import Veiculo

@app.route('/') # o símbolo "@" significa "Decorador" - Basicamente está dizendo: "Flask, fique de olho na porta principal (/). Se alguém entrar, execute a função abaixo."
def index():
    return render_template('index.html')

@app.route('/veiculos')
def listar_veiculos():

    # Buscamos todos os veículos do banco de dado
    lista_de_veiculos = Veiculo.query.all()

    # Passamos a lista para o HTML através da variável 'veiculos'
    return render_template('ConsultaDeVeiculos.html', veiculos = lista_de_veiculos)