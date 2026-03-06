from app import create_app

app = create_app()

if __name__ == "__main__":
    # O debug=True permite que o site reinicie sozinho quando você salvar um arquivo
    app.run(debug=True)