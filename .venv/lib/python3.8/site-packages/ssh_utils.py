import paramiko


class SSHManager:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.client = paramiko.SSHClient()

    def connect(self):
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.host, username=self.username, password=self.password)

    def disconnect(self):
        if self.client:
            self.client.close()

    def execute_command(self, command):
        """Execute an SSH command and return the output"""
        self.connect()
        stdin, stdout, stderr = self.client.exec_command(command)
        output = stdout.read().decode('utf-8')
        self.disconnect()
        return output
