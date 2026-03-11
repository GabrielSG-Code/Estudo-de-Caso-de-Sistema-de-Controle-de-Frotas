from app import create_app
from app.models import db, Veiculo, TipoCombustível, StatusVeiculo

app = create_app()

def popular():
    with app.app_context():
        v1 = Veiculo(
            placa='ABC1E23', 
            modelo='Chevrolet Onix', 
            marca='Chevrolet',
            ano=2023,
            tipoVeiculo='Passeio',
            combustivel=TipoCombustível.GASOLINA,
            Km_Atual=15000.0,
            Km_UltimaTrocaOleo=10000.0,
            Km_UltimaRevisao=10000.0,
            status=StatusVeiculo.ATIVO)
        
        v2 = Veiculo(
            placa='XYZ5678', 
            modelo='Volkswagen Gol', 
            marca='Volkswagen',
            ano=2021,
            tipoVeiculo='Passeio',
            combustivel=TipoCombustível.ETANOL,
            Km_Atual=45000.0,
            Km_UltimaTrocaOleo=40000.0,
            Km_UltimaRevisao=40000.0,
            status=StatusVeiculo.MANUTENCAO)


        db.session.add(v1)        
        db.session.add(v2)

        db.session.commit()

        print("Banco de dados populado com sucesso!")

if __name__ == '__main__':
    popular()       