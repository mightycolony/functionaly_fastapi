import paramiko


def ssh_connection(ip,username,password,cmd):
    try:
        print(ip,username,password,cmd)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip,username=username,password=password)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        err = ''.join(stdout.readlines())
        out = ''.join(stdout.readlines())
        return (out,err)
    except Exception as e:
        return  e

    


ssh_connection("192.168.1.18","notu","notu","uname")

