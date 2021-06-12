
class Email():
    def __init__(self):
        pass
    def prepare(self):
        pass
    def send(self):
        pass

class ServiceNow():
    def __init__(self):
        pass
    def raise_ticket(self):
        pass
    def prepare(self):
        pass

class Restart():
    def __init__(self):
        import paramiko,time
        import os
        HOST = os.getenv("WIN", "13.70.2.146")
        USER = os.getenv("WIN_USER", "tagler")
        PWD = os.getenv("WIN_PASW", "Tagler@12345")
        # initialize the ssh client

        ssh_client = paramiko.SSHClient()
        # enable host auto-add policy
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # connect to windows server
        ssh_client.connect(hostname =HOST, username = USER, password = PWD, port = 22)
        # execute the script on windows server
        time.sleep(10)
        stdin, stdout, stderr = ssh_client.exec_command('taskkill /IM "msedge.exe" /F')
        time.sleep(10)
        stdin, stdout, stderr = ssh_client.exec_command('PsExec.exe -u '+USER+' -p '+ PWD +' -i 2 -d ""C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe""')
        # print the standard out and error (if any) 
        print('stdout -- ', stdout.read())
        print('stderr -- ', stderr.read())