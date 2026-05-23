from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
# Configura o banco de dados (será criado um arquivo chamado 'estoque.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estoque.db'
db = SQLAlchemy(app)

# Definindo a estrutura da tabela
class Medicamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    lote = db.Column(db.String(50), nullable=False)
    fabricacao = db.Column(db.Date, nullable=False)
    validade = db.Column(db.Date, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)

# Cria o banco de dados na primeira vez que rodar
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    # Busca todos os medicamentos do banco
    medicamentos = Medicamento.query.all()
    
    # Processa a lógica de status para exibir no HTML
    lista_exibicao = []
    hoje = datetime.now().date()
    for med in medicamentos:
        limite = hoje + timedelta(days=30)
        status, classe = "OK", "ok"
        if med.validade < hoje:
            status, classe = "Vencido", "vencido"
        elif hoje <= med.validade <= limite:
            status, classe = "Próximo", "proximo"
        
        lista_exibicao.append({
            'nome': med.nome, 'lote': med.lote, 'fab': med.fabricacao,
            'val': med.validade, 'qtd': med.quantidade, 'status': status, 'classe': classe
        })
    return render_template('index.html', medicamentos=lista_exibicao)

@app.route('/salvar', methods=['POST'])
def salvar():
    # Converte string para data antes de salvar
    nova_med = Medicamento(
        nome=request.form['nome'],
        lote=request.form['lote'],
        fabricacao=datetime.strptime(request.form['fabricacao'], '%Y-%m-%d'),
        validade=datetime.strptime(request.form['validade'], '%Y-%m-%d'),
        quantidade=request.form['quantidade']
    )
    db.session.add(nova_med)
    db.session.commit()
    return redirect('/')