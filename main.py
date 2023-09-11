from flask import Flask, render_template, request, session, redirect, url_for,jsonify
from connection_ssh import connect_ssh, disconnect_ssh
import uuid
import requests
from flask_cors import CORS  # Importe a extensão Flask-CORS
import pandas as pd
from datetime import datetime, timedelta
import sqlite3
Logado = False
app = Flask(__name__)
CORS(app) 
CORS(app, resources={r"/get_system_data": {"origins": "http://127.0.0.1:5000"}})

app.secret_key = str(uuid.uuid4())



#get_data_cpu() envia os dados de % de uso da CPU dos ultimos 60 segundos que estão no banco para a interface
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

#get_data_disco envia os dados de % de uso do Disco dos ultimos 60 segundos que estão no banco para a interface
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

#get_data_memoria() envia os dados de % de uso da memória dos ultimos 60 segundos que estão no banco para a interface
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


#get_data_swap() envia os dados de % de uso do swap dos ultimos 60 segundos que estão no banco para a interface
@app.route('/swap-data', methods=['GET'])
def get_data_swap():
    conn = sqlite3.connect('dados/banco.db')
    cursor = conn.cursor()
    
    now = datetime.now()
    timestamp_60_seconds_ago = now - timedelta(seconds=62)
    
    timestamp_60_seconds_ago_str = timestamp_60_seconds_ago.strftime('%d-%m-%Y %H:%M:%S')
    
    cursor.execute('SELECT DataHora,ROUND((Swap_usada / Swap_total) * 100, 2) AS porcent_swap  FROM memoria WHERE DataHora >= ?', (timestamp_60_seconds_ago_str,))
    data = cursor.fetchall()
    conn.close()
    
    df = pd.DataFrame(data, columns=['DataHora', 'porcent_swap'])
    data_hora = (((df['DataHora']).str.split().str[1]).tolist())
    swap_usada = ((df['porcent_swap']).astype(float).tolist())
    
    swap_data = pd.DataFrame({'Timestamp': data_hora, 'SwapUsage': swap_usada})
    
    data = {
        'timestamp': swap_data['Timestamp'].tolist(),
        'swap_usage': swap_data['SwapUsage'].tolist()
    } 
    return jsonify(data)
#Interface do sistema onde os gráficos são exibidos 
@app.route('/')
def home():
    global Logado
    if Logado == True:
        return render_template('dados_mainframe.html')
    else:
        return redirect(url_for("login"))
        
 #Envia os dados do mainframe em tempo real para a interface
@app.route('/get_system_data', methods=["GET"])
def get_system_data():
    url = "http://127.0.0.1:5020/get_system_data"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            system_data = response.json()
            return jsonify(system_data)
        else:
            return "Erro ao obter os dados ", 500
    except requests.exceptions.RequestException as e:
        return "Erro na solicitação para http://127.0.0.1:5020: " + str(e), 500
    


#Captura os dados do formulário para fazer o login usando chaves SSH
@app.route("/login", methods=["GET", "POST"])
def login():
    global Logado
    if  Logado == False:
        if request.method == "POST":
            
            hostname = request.form["hostname"]
            username = request.form["username"]
            ssh = connect_ssh(hostname, username)

            if ssh:
                Logado = True
        
                session["hostname"] = hostname
                session["username"] = username
                return redirect(url_for("home")) 
                
            else:
                
                return render_template("login.html", error="Erro de autenticação")

        return render_template("login.html")
    else:
        return redirect(url_for("home"))
       
#Chama a função disconnect_ssh() para fazer logout do usuário
@app.route("/logout", methods=["GET", "POST"])
def logout():
    global Logado
    
    disconnect_ssh(session.get("ssh"))
    session.clear()
    Logado =False
    return redirect(url_for("login"))



if __name__ == "__main__":
    app.run(debug=True)
