import os
from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import requests
from datetime import date, timedelta, datetime
from calculadora_ig import IdadeGestacional

app = Flask(__name__)


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
    # nova_fita = Urina(nome=nome, email=email, foto_fita=foto_fita_bytes)
    # db.session.add(nova_fita)
    # db.session.commit()
    # Renderiza a página de exibição da imagem
    return render_template('view.html', filename=filename)

@app.route('/questionario_urina')
def questionario_urina():
    return render_template('questionario_urina.html')

@app.route('/submit_questionario_urina', methods=['POST'])
def submit_questionario_urina():
    question1 = request.form.get('question1')
    question2_input = request.form.get('question2_input')
    question3 = request.form.getlist('question3[]')
    question4 = request.form.get('question4')
    question5 = request.form.get('question5')
    question6_input = request.form.get('question6_input')

    question3_str = ','.join(question3)
    print(question1, question2_input, question3, question3_str, question4, question5, question6_input)
    return redirect(url_for('home'))

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
    idade_calculada_pelo_usg, semanas_usg, dias_usg, data_parto_usg = ig.calcular_idade_gestacional_pelo_ultrassom()
    idade_calculada_pela_dum, semanas_dum, dias_dum, data_parto_dum = ig.calcular_idade_gestacional_pela_dum()
    metodo, idade_final, outra_ig, outro_metodo = ig.qual_ig_usar()
    #Definindo a cor do card
    if metodo == "DUM":
        print(metodo)
        usg_verde = ""
        dum_verde = "background-color: #00AA9E;"
    else:
        print(metodo)
        usg_verde = "background-color: #00AA9E;"
        dum_verde = ""
    return render_template("resultado_ig.html", metodo=metodo, ig_dum=idade_calculada_pela_dum, ig_usg=idade_calculada_pelo_usg, usg_verde=usg_verde, dum_verde=dum_verde)



#############################

if __name__ == "__main__":
    app.run(debug=True, port=8080)
