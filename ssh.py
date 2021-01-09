import paramiko
import sys

hostname = "34.107.36.105"

port = 22

username = "merto"

password = "pizza"

command = 'ls'



try:
    client = paramiko.SSHClient()
    #client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 

    client.connect(hostname, port=port, username=username, password=password)

    stdin, stdout, stderr = client.exec_command(command)
   
    output = stdout.read().decode('utf-8').splitlines()
    print (output)


except Exception as e:
    #print(e)
    trace_back = sys.exc_info()[2]
    line = trace_back.tb_lineno
    print(format(line),e)   

finally:
    stdin.close()
    client.close()