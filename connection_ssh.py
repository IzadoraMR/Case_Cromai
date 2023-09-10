import paramiko
import os
import json
arquivo_json = "config.json"

def connect_ssh(hostname, username):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username=username, allow_agent=True)
        data = {
        "hostname": hostname,
        "username": username
        }
        with open(arquivo_json, "w") as json_file:
            json.dump(data, json_file)
        message = "true"
        stdin, stdout, stderr = ssh.exec_command('ls')
        print(stdout.readlines())
        return ssh, message
    except paramiko.ssh_exception.AuthenticationException:
        message = "false"
        return None, message  # Retorna None para indicar que a autenticação falhou

def disconnect_ssh(ssh):
    with open(arquivo_json, "w") as json_file:
        pass
    if ssh is not None:
        ssh.close()
       
