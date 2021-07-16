import paramiko

def ssh_cli(ip,username,password,port=22,cmd='show run'):
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip,port=port,username=username,password=password,timeout=5,compress=True)
    stdin,stdout,stderr = ssh.exec_command(cmd)
    x = stdout.read().decode()
    return x

if __name__ == '__main__':
    # print(ssh_cli('1.1.1.128','root','123456'))
    print(ssh_cli('1.1.1.200','cisco','cisco',cmd='show run'))