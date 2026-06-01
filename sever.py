from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta # <-- Adicionamos o timedelta aqui

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estoque.db'
db = SQLAlchemy(app)

class Medicamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    lote = db.Column(db.String(50), nullable=False)
    fabricacao = db.Column(db.Date, nullable=False)
    validade = db.Column(db.Date, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    # TRUQUE: O 'order_by' faz os remédios que vencem primeiro aparecerem no topo!
    todos_medicamentos = Medicamento.query.order_by(Medicamento.validade).all()
    
    # Calculando as datas para o alerta
    hoje = datetime.now().date()
    limite_alerta = hoje + timedelta(days=90) # Alerta para 90 dias
    
    # Enviamos os remédios, o dia de hoje e o limite lá para o site (HTML)
    return render_template('index.html', medicamentos=todos_medicamentos, hoje=hoje, limite_alerta=limite_alerta)

@app.route('/salvar', methods=['POST'])
def salvar():
    try:
        nome = request.form['nome']
        lote = request.form['lote']
        fabricacao = datetime.strptime(request.form['fabricacao'], '%Y-%m-%d').date()
        validade = datetime.strptime(request.form['validade'], '%Y-%m-%d').date()
        quantidade = request.form['quantidade']

        if fabricacao >= validade:
            return """
                <h3 style="color: red; font-family: Arial;">Erro: A data de fabricação não pode ser maior ou igual à validade.</h3>
                <a href="/" style="font-family: Arial; color: blue;">Voltar para a tela inicial</a>
            """

        novo_medicamento = Medicamento(nome=nome, lote=lote, fabricacao=fabricacao, validade=validade, quantidade=quantidade)
        db.session.add(novo_medicamento)
        db.session.commit() 
        
    except Exception as e:
        print(f"Erro ao salvar: {e}")

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)