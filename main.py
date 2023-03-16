import os
from flask import Flask, render_template, request, send_from_directory
import requests
from datetime import date, timedelta, datetime
from calculadora_ig import IdadeGestacional
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Configuração do SQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///teste-urina.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuração do banco de dados SQLAlchemy
db = SQLAlchemy(app)

# Definição do modelo de dados
class Urina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(80), nullable=False)
    foto_fita = db.Column(db.LargeBinary)

    def __repr__(self):
        return '<Book %r>' % self.nome

# Criação do banco de dados
with app.app_context():
    db.create_all()

## PASTA PARA UPLOADS DE FOTO SEM SER NO DB SQL ##
app.config['uploads'] = 'uploads' # Diretório onde as imagens serão armazenadas

#### PÁGINA PRINCIPAL ####
@app.route('/')
def main():
    return render_template('index.html')


#### PEGAR IMAGEM - MINUTO TESTE #####

@app.route('/capturar')
def capturar():
    return render_template('captura_imagem.html')

@app.route('/upload', methods=['POST'])
def upload():
    #Pega os dados
    nome = request.form["name"]
    email = request.form["email"]
    # Salva a imagem enviada no diretório uploads
    foto_fita = request.files['foto_fita']
    filename = foto_fita.filename
    foto_fita.save(os.path.join(app.config['uploads'], filename))
    foto_fita_bytes = request.files['foto_fita'].read()  # converte FileStorage em bytes
    nova_fita = Urina(nome=nome, email=email, foto_fita=foto_fita_bytes)
    db.session.add(nova_fita)
    db.session.commit()
    # Renderiza a página de exibição da imagem
    return render_template('view.html', filename=filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # Retorna a imagem armazenada no diretório uploads
    return send_from_directory(app.config['uploads'], filename)



##### CALCULADORA IG ########
@app.route('/calculadora')
def calculadora():
    return render_template('calcular.html')

@app.route('/calcular', methods=['POST'])
def calcular_idade_gestacional():
    data_ultima_menstruacao = date.fromisoformat(request.form['data_ultima_menstruacao'])
    data_primeiro_ultrassom = date.fromisoformat(request.form['data_primeiro_ultrassom'])
    idade_gestacional_ultrassom = int(request.form['idade_gestacional_ultrassom_semanas'])*7+int(request.form['idade_gestacional_ultrassom_dias'])
    ig = IdadeGestacional(data_ultima_menstruacao, data_primeiro_ultrassom, idade_gestacional_ultrassom)
    metodo, idade_final, outra_ig, outro_metodo = ig.qual_ig_usar()

    return f"<h1> Utilizar IG({metodo}): {idade_final} / IG({outro_metodo}): {outra_ig} <h1>"



#############################

if __name__ == "__main__":
    app.run(debug=True)
