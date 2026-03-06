from app import create_app
from app.models import db, Veiculo

app = create_app()

def popular():
    with app.app_context():
        v1 = Veiculo(modelo='Chevrolet Onix', placa='ABC-1E23', status='Disponível')
        v2 = Veiculo(modelo='Volkswagen Gol', placa='XYZ-5678', status='Manutenção')
        v3 = Veiculo(modelo='Fiat Fiorino', placa='KLU-1478', status='Disponível')

        db.session.add(v1)        
        db.session.add(v2)
        db.session.add(v3)

        db.session.commit

        print("Banco de dados populado com sucesso!")

if __name__ == '__main__':
    popular()       