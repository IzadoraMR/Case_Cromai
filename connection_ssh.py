import paramiko
import json
arquivo_json = "config.json"


#Função responsável pela autenticação do usuário 
def connect_ssh(hostname, username):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, port = 22,username=username, allow_agent=True)
        data = {
        "hostname": hostname,
        "username": username
        }
        with open(arquivo_json, "w") as json_file:
            json.dump(data, json_file)
        stdin, stdout, stderr = ssh.exec_command('ls')
        print(stdout.readlines())
        print("Verificação Login")
        return ssh
    except paramiko.ssh_exception.AuthenticationException:
        return None 
    
    
#Função responsável pelo logout do usuário
def disconnect_ssh(ssh):
    with open(arquivo_json, "w") as json_file:
        pass
    if ssh is not None:
        ssh.close()
       
