import paramiko,time

# initialize the ssh client

ssh_client = paramiko.SSHClient()
# enable host auto-add policy
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# connect to windows server
ssh_client.connect(hostname ="13.70.2.146", username = "tagler", password = "Tagler@12345", port = 22)
# execute the script on windows server
time.sleep(3)
stdin, stdout, stderr = ssh_client.exec_command('taskkill /IM "msedge.exe" /F')
time.sleep(3)
stdin, stdout, stderr = ssh_client.exec_command('query session tagler')
s = stdout.read().decode("utf-8")
s = s[s.index("tagler")+6:s.index("Active")].strip()
stdin, stdout, stderr = ssh_client.exec_command('PsExec.exe -u 13.70.2.146\Tagler -p Tagler@12345 -i '+s+' -d "C:/PSTools/script/msedge.bat"')
# print the standard out and error (if any) 
time.sleep(5)
print('stdout -- ', stdout.read().decode("utf-8"))
print('stderr -- ', stderr.read())