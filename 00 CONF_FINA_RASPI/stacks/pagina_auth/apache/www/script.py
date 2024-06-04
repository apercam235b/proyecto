import paramiko

hostname = '192.168.1.11'
port = 22
username = 'root'
password = 'departamento'

client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(hostname=hostname, port=port, username=username, password=password)
    stdin, stdout, stderr = client.exec_command('python3 /opt/scripts/socket_cliente.py')
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')

finally:
    client.close()
