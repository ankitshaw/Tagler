import paramiko,time

# initialize the ssh client

ssh_client = paramiko.SSHClient()
# enable host auto-add policy
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# connect to windows server
ssh_client.connect(hostname ="13.70.2.146", username = "tagler", password = "Tagler@12345", port = 22)
# execute the script on windows server
time.sleep(10)
stdin, stdout, stderr = ssh_client.exec_command('taskkill /IM "msedge.exe" /F')
time.sleep(10)
stdin, stdout, stderr = ssh_client.exec_command('PsExec.exe -u Tagler -p Tagler@12345 -i 2 -d ""C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe""')
# print the standard out and error (if any) 
print('stdout -- ', stdout.read())
print('stderr -- ', stderr.read())