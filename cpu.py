from flask import Flask, render_template, jsonify, request
import paramiko
import json
import pandas as pd
from flask_cors import CORS  
import sqlite3
import datetime


app = Flask(__name__)
CORS(app, resources={r"/get_system_data": {"origins": "http://127.0.0.1:5000"}})

arquivo_json = "config.json"
cpu_command = "mpstat -P ALL 1 1 | grep -v 'Média'"
disk_command = "df -h /"
memory_command = "free -m"



def system():
    conexao = sqlite3.connect("dados/banco.db")
    cursor = conexao.cursor()
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_agent = paramiko.Agent()
    with open(arquivo_json, "r") as json_file:
        dados = json.load(json_file)
    hostname = dados["hostname"]
    username = dados["username"]

    ssh.connect(hostname, username=username, allow_agent=True)
    hora = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    # CPU ------------------------------------------------------------------------------
    stdin, stdout, stderr = ssh.exec_command(cpu_command)
    cpu_info = stdout.read().decode()

    lines = cpu_info.strip().split('\n')
    header = lines[2].split()
    data = [line.split() for line in lines[3:]]
    df = pd.DataFrame(data, columns=header)
    df = df.iloc[:, [0, 1, 11]]

    TotalCPU = round(100 - float(df.iloc[0, -1].replace(',', '.')), 2)
    CPU1 = round(100 - float(df.iloc[1, -1].replace(',', '.')), 2)
    CPU2 = round(100 - float(df.iloc[2, -1].replace(',', '.')), 2)
    CPU3 = round(100 - float(df.iloc[3, -1].replace(',', '.')), 2)
    CPU4 = round(100 - float(df.iloc[4, -1].replace(',', '.')), 2)
   
    cursor.execute("INSERT INTO CPU (DataHora, CPU1, CPU2, CPU3, CPU4, CPUTotal) VALUES (?, ?, ?, ?, ?, ?)",
               (hora, CPU1, CPU2, CPU3, CPU4, TotalCPU))
    conexao.commit()
    # Disco ------------------------------------------------------------------------------
    hora = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    stdin, stdout, stderr = ssh.exec_command(disk_command)
    disk_info = stdout.read().decode()
    lines_disco = disk_info.strip().split('\n')
    header_disco= lines_disco[1].split()
    TamDisco = header_disco[1][:-1]
    UsoDisco = header_disco[2][:-1]
    dispDisco = header_disco[3][:-1]
    UsoDiscoP = header_disco[4][:-1]
    
    cursor.execute("INSERT INTO Disco (DataHora, Disco_total, Disco_usado, Disco_disponivel, Porcen_usada) VALUES (?, ?, ?, ?, ?)",
               (hora, TamDisco, UsoDisco, dispDisco, UsoDiscoP))
    conexao.commit()
    #Memória ------------------------------------------------------------------------------
    hora = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    stdin, stdout, stderr = ssh.exec_command(memory_command)
    memory_info = stdout.read().decode()
    
    lines_mem = memory_info.strip().split('\n')
    header_mem = lines_mem[1].split()
    header_Swap = lines_mem[2].split()
    memTotal = header_mem[1]
    memUsada = header_mem[2]
    memLivre = header_mem[3]
    memCompart = header_mem[4]
    memCache = header_mem[5]
    memDispo = header_mem[6]
    swapTotal = header_Swap[1]
    swapUsada = header_Swap[2]
    swapLivre = header_Swap[3]
    cursor.execute("INSERT INTO Memoria (DataHora, Memoria_total, Memoria_usada, Memoria_livre, Memoria_compartilhada, Memoria_cache, Memoria_disponivel, Swap_total, Swap_usada, Swap_livre) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
               (hora, memTotal, memUsada, memLivre, memCompart, memCache, memDispo, swapTotal, swapUsada, swapLivre))
    conexao.commit()
    dados = {
            "CPU1": CPU1,
            "CPU2": CPU2,
            "CPU3": CPU3,
            "CPU4": CPU4,
            "TotalCPU": TotalCPU,
            "TamDisco": TamDisco,
            "UsoDisco": UsoDisco,
            "UsoDiscoP": UsoDiscoP,
            "dispDisco":dispDisco,
            "memTotal":memTotal,
            "memUsada":memUsada,
            "memLivre":memLivre,
            "memCompart":memCompart,
            "memCache":memCache,
            "memDispo":memDispo,
            "swapTotal":swapTotal,
            "swapUsada":swapUsada,
            "swapLivre": swapLivre
            
            
            
            
            
        }
    conexao.close()
    return dados

@app.route('/')
def index():
    return "Servidor Flask em execução em http://127.0.0.1:5020."

@app.route('/get_system_data', methods=["GET"])
def get_cpu_data():
    cpu_info = system()
    return jsonify(cpu_info), 200


if __name__ == '__main__':
     app.run(host='127.0.0.1', port=5020, debug=True)
