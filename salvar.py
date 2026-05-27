from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

# 1. Configurando o Servidor e o Banco de Dados
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estoque.db'
db = SQLAlchemy(app)

# 2. Criando o modelo da Tabela no Banco de Dados
class Medicamento(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    lote = db.Column(db.String(50), nullable=False)
    fabricacao = db.Column(db.Date, nullable=False)
    validade = db.Column(db.Date, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)

# Cria o arquivo estoque.db caso ele não exista
with app.app_context():
    db.create_all()

# 3. Rota Principal (Página Inicial)
@app.route('/')
def index():
    # Pega todos os itens do banco de dados
    medicamentos_db = Medicamento.query.all()
    lista_exibicao = []
    hoje = datetime.now().date()
    limite = hoje + timedelta(days=90) # Alerta de 90 dias

    for med in medicamentos_db:
        status, classe = "OK", "ok"
        if med.validade < hoje:
            status, classe = "Vencido", "vencido"
        elif hoje <= med.validade <= limite:
            status, classe = "Próximo", "proximo"
        
        lista_exibicao.append({
            'id': med.id, 'nome': med.nome, 'lote': med.lote, 
            'fab': med.fabricacao, 'val': med.validade, 
            'qtd': med.quantidade, 'status': status, 'classe': classe
        })
        
    return render_template('index.html', medicamentos=lista_exibicao)

# 4. Rota para Salvar os Dados do HTML
@app.route('/salvar', methods=['POST'])
def salvar():
    try:
        data_fab = datetime.strptime(request.form['fabricacao'], '%Y-%m-%d').date()
        data_val = datetime.strptime(request.form['validade'], '%Y-%m-%d').date()

        # Impede cadastro se a fabricação for depois da validade
        if data_fab >= data_val:
            return "Erro: Data de fabricação não pode ser maior que a validade. Volte e tente novamente."

        novo_med = Medicamento(
            nome=request.form['nome'],
            lote=request.form['lote'],
            fabricacao=data_fab,
            validade=data_val,
            quantidade=request.form['quantidade']
        )
        db.session.add(novo_med)
        db.session.commit()
    except Exception as e:
        print(f"Erro ao salvar: {e}")

    # Salva e volta para a página principal
    return redirect('/')

# 5. LIGANDO O SERVIDOR (Isso é o que faz o Flask abrir!)
if __name__ == '__main__':
    app.run(debug=True)