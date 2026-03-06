from flask import current_app as app # Importa o app que está rodando
from flask import render_template

@app.route('/') # o símbolo "@" significa "Decorador" - Basicamente está dizendo: "Flask, fique de olho na porta principal (/). Se alguém entrar, execute a função abaixo."
def index():
    return render_template('index.html')

@app.route('/veiculos')
def listar_veiculos():
    return "<h3>Aqui aparecerá a lista de veículos da sua planilha em breve!</h3>"