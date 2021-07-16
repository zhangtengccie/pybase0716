import hashlib
import re
from ssh_router import ssh_cli
import time



def qytang_get_config(ip,username='cisco',password='cisco'):
    try:
        device_config = ssh_cli(ip, username, password)
        ret = re.split(r'\nhostname \S+\n', device_config)
        run_conf = re.findall('hostname.*',str(ret))
        m = hashlib.md5()
        m.update(str(run_conf).encode())
        md5_value = m.hexdigest()
        return md5_value

    except Exception:
        return

def qytang_check_diff(ip,username='cisco',password='cisco'):
    before_md5=''
    while True:
        before_md5=qytang_get_config(ip,username,password)
        time.sleep(5)
        now_md5 = qytang_get_config(ip,username,password)
        print(now_md5)
        if before_md5 != now_md5:
            print('MD5 value changed')



if __name__ == '__main__':
    qytang_check_diff('1.1.1.200')
