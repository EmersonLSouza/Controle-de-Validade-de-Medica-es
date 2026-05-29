from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# ================= CONFIGURAÇÕES =================
app = Flask(__name__)
# Diz ao Flask para criar e usar o banco de dados estoque.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estoque.db'
db = SQLAlchemy(app)

# ================= TABELA DO BANCO DE DADOS =================
class Medicamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    lote = db.Column(db.String(50), nullable=False)
    fabricacao = db.Column(db.Date, nullable=False)
    validade = db.Column(db.Date, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)

# Cria o arquivo estoque.db automaticamente se ele não existir
with app.app_context():
    db.create_all()

# ================= ROTA 1: MOSTRAR O SITE =================
@app.route('/')
def index():
    # Vai no banco de dados e puxa todos os medicamentos cadastrados
    todos_medicamentos = Medicamento.query.all()
    # Envia os dados para preencher a tabela do index.html
    return render_template('index.html', medicamentos=todos_medicamentos)

# ================= ROTA 2: SALVAR NO BANCO DE DADOS =================
@app.route('/salvar', methods=['POST'])
def salvar():
    try:
        # 1. Puxando as informações que foram digitadas no formulário do site
        nome = request.form['nome']
        lote = request.form['lote']
        fabricacao = datetime.strptime(request.form['fabricacao'], '%Y-%m-%d').date()
        validade = datetime.strptime(request.form['validade'], '%Y-%m-%d').date()
        quantidade = request.form['quantidade']

        # 2. Trava de segurança: A validade tem que ser maior que a fabricação
        if fabricacao >= validade:
            return """
                <h3 style="color: red; font-family: Arial;">Erro: A data de fabricação não pode ser maior ou igual à validade.</h3>
                <a href="/" style="font-family: Arial; color: blue;">Voltar para a tela inicial</a>
            """

        # 3. Preparando o pacote de dados
        novo_medicamento = Medicamento(
            nome=nome, 
            lote=lote, 
            fabricacao=fabricacao, 
            validade=validade, 
            quantidade=quantidade
        )
        
        # 4. Salvando definitivamente no arquivo estoque.db
        db.session.add(novo_medicamento)
        db.session.commit() 
        
    except Exception as e:
        print(f"Erro ao salvar: {e}")

    # 5. Após salvar, redireciona o usuário de volta para a tela inicial automaticamente
    return redirect('/')

# ================= LIGAR O SERVIDOR =================
if __name__ == '__main__':
    app.run(debug=True)