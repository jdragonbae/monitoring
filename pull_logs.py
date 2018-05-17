import subprocess


servers = ['10.41.2.31', '10.41.1.25', '10.41.5.49', '10.41.2.41', '10.41.0.232', '10.41.5.67', '10.41.2.84', '10.41.0.162', '10.41.5.74']

for server in servers:
    cmd = subprocess.Popen("sshpass -p gorepdl123 scp hackday@"+server+":hackday.log logs/"+server+".log", shell=True, stdout=subprocess.PIPE)
