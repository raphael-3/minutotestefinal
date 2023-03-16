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
    hoje = datetime.today().date()
    return render_template('calcular.html', hoje=hoje)

@app.route('/calcular', methods=['POST'])
def calcular_idade_gestacional():
    #Pegando os inputs
    data_ultima_menstruacao = date.fromisoformat(request.form['data_ultima_menstruacao'])
    data_primeiro_ultrassom = date.fromisoformat(request.form['data_primeiro_ultrassom'])
    idade_gestacional_ultrassom = int(request.form['idade_gestacional_ultrassom_semanas'])*7+int(request.form['idade_gestacional_ultrassom_dias'])
    #calculos da calculadora
    ig = IdadeGestacional(data_ultima_menstruacao, data_primeiro_ultrassom, idade_gestacional_ultrassom)
    idade_calculada_pelo_usg, dias_usg, data_parto_usg = ig.calcular_idade_gestacional_pelo_ultrassom()
    idade_calculada_pela_dum, dias_dum, data_parto_dum = ig.calcular_idade_gestacional_pela_dum()
    metodo, idade_final, outra_ig, outro_metodo = ig.qual_ig_usar()
    #Definindo a cor do card
    if metodo == "DUM":
        usg_verde = ""
        dum_verde = "background-color: #00AA9E;"
    else:
        usg_verde = "background-color: #00AA9E;"
        dum_verde = ""
    return render_template("resultado_ig.html", metodo=metodo, ig_dum=idade_calculada_pela_dum, ig_usg=idade_calculada_pelo_usg, usg_verde=usg_verde, dum_verde=dum_verde)



#############################

if __name__ == "__main__":
    app.run(debug=True, port=8000)
