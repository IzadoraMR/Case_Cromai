from flask import Flask, render_template, request, session, redirect, url_for,jsonify
from connection_ssh import connect_ssh, disconnect_ssh
import uuid
import requests
from flask_cors import CORS  # Importe a extensão Flask-CORS
import pandas as pd
from datetime import datetime, timedelta
import sqlite3

app = Flask(__name__)
CORS(app) 
CORS(app, resources={r"/get_system_data": {"origins": "http://127.0.0.1:5000"}})

app.secret_key = str(uuid.uuid4())


# Função para verificar se o usuário está logado
def is_logged_in():
    return "hostname" in session and "username" in session

@app.route('/cpu-data', methods=['GET'])
def get_data_cpu():
    conn = sqlite3.connect('dados/banco.db')
    cursor = conn.cursor()
    
    now = datetime.now()
    timestamp_60_seconds_ago = now - timedelta(seconds=62)
    
    timestamp_60_seconds_ago_str = timestamp_60_seconds_ago.strftime('%d-%m-%Y %H:%M:%S')
    
    cursor.execute('SELECT DataHora, CPUTotal FROM CPU WHERE DataHora >= ?', (timestamp_60_seconds_ago_str,))
    data = cursor.fetchall()
    conn.close()
    
    df = pd.DataFrame(data, columns=['DataHora', 'CPUTotal'])
    data_hora = (((df['DataHora']).str.split().str[1]).tolist())
    cpu_total = ((df['CPUTotal']).astype(float).tolist())
    
    cpu_data = pd.DataFrame({'Timestamp': data_hora, 'CPUUsage': cpu_total})
    
    data = {
        'timestamp': cpu_data['Timestamp'].tolist(),
        'cpu_usage': cpu_data['CPUUsage'].tolist()
    } 
    return jsonify(data)

@app.route('/disco-data', methods=['GET'])
def get_data_disco():
    conn = sqlite3.connect('dados/banco.db')
    cursor = conn.cursor()
    
    now = datetime.now()
    timestamp_60_seconds_ago = now - timedelta(seconds=62)
    
    timestamp_60_seconds_ago_str = timestamp_60_seconds_ago.strftime('%d-%m-%Y %H:%M:%S')
    
    cursor.execute('SELECT DataHora, Porcen_usada FROM Disco WHERE DataHora >= ?', (timestamp_60_seconds_ago_str,))
    data = cursor.fetchall()
    conn.close()
    
    df = pd.DataFrame(data, columns=['DataHora', 'DiscoUsado'])
    data_hora = (((df['DataHora']).str.split().str[1]).tolist())
    disco_usado = ((df['DiscoUsado']).astype(float).tolist())
    
    disco_data = pd.DataFrame({'Timestamp': data_hora, 'DiscoUsage': disco_usado})
    
    data = {
        'timestamp': disco_data['Timestamp'].tolist(),
        'disco_usage': disco_data['DiscoUsage'].tolist()
    } 
    return jsonify(data)

@app.route('/memoria-data', methods=['GET'])
def get_data_memoria():
    conn = sqlite3.connect('dados/banco.db')
    cursor = conn.cursor()
    
    now = datetime.now()
    timestamp_60_seconds_ago = now - timedelta(seconds=62)
    
    timestamp_60_seconds_ago_str = timestamp_60_seconds_ago.strftime('%d-%m-%Y %H:%M:%S')
    
    cursor.execute('SELECT DataHora,ROUND((memoria_usada / memoria_total) * 100, 2) AS porcent_memoria  FROM memoria WHERE DataHora >= ?', (timestamp_60_seconds_ago_str,))
    data = cursor.fetchall()
    conn.close()
    
    df = pd.DataFrame(data, columns=['DataHora', 'porcent_memoria'])
    data_hora = (((df['DataHora']).str.split().str[1]).tolist())
    memoria_usada = ((df['porcent_memoria']).astype(float).tolist())
    
    memoria_data = pd.DataFrame({'Timestamp': data_hora, 'MemoriaUsage': memoria_usada})
    
    data = {
        'timestamp': memoria_data['Timestamp'].tolist(),
        'memoria_usage': memoria_data['MemoriaUsage'].tolist()
    } 
    return jsonify(data)

@app.route('/')
def home():
    return render_template('cpu.html')
 
@app.route('/get_system_data', methods=["GET"])
def get_cpu_data():

    url = "http://127.0.0.1:5020/get_system_data"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            cpu_data = response.json()
            return jsonify(cpu_data)
        else:
            return "Erro ao obter os dados da CPU", 500
    except requests.exceptions.RequestException as e:
        return "Erro na solicitação para http://127.0.0.1:5020: " + str(e), 500
    

@app.route("/about")
def about():
    if is_logged_in():
        return render_template("about.html")
    else:
        return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if not is_logged_in():
        if request.method == "POST":
            # Obtenha os dados do formulário
            hostname = request.form["hostname"]
            username = request.form["username"]

            # Tente criar uma conexão SSH (substitua esta linha com sua lógica de autenticação)
            ssh = connect_ssh(hostname, username)

            if ssh:
                # Armazene informações relevantes na sessão
                session["hostname"] = hostname
                session["username"] = username

                # Redirecione para a página inicial após o login
                return redirect(url_for("home"))
            else:
                # Se a conexão SSH falhar, redirecione de volta para a página de login com uma mensagem de erro
                return render_template("login.html", error="Erro de autenticação")

        return render_template("login.html")
    else:
        return redirect(url_for("login"))
       

@app.route("/logout", methods=["GET", "POST"])
def logout():
    # Você deve adicionar sua lógica de desconexão SSH aqui (substitua esta linha)
    disconnect_ssh(session.get("ssh"))
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
