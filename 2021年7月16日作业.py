import re
import sqlite3
import os
import hashlib
from ssh_router import ssh_cli
import time



def qytang_get_md5(ip,username='cisco',password='cisco'):
    try:
        device_config_raw = ssh_cli(ip,username,password,cmd='show run')
        split_result = re.split(r'\r\nhostname \S+\r\n',device_config_raw)
        device_config = device_config_raw.replace(split_result[0], '').strip()
        m = hashlib.md5()
        m.update(device_config.encode())
        md5_value = m.hexdigest()
        return device_config,md5_value
    except Exception:
        return



device_list = ['1.1.1.200']
username = 'cisco'
password = 'cisco'

def write_config_md5_to_db():
    conn = sqlite3.connect('homeworkdb.sqlite')
    cursor = conn.cursor()
    for device in device_list:
        config_and_md5 = qytang_get_md5(device,username,password)
        cursor.execute('select * from config where ip=?',(device,))
        md5_result = cursor.fetchall()
        if not md5_result:
            cursor.execute("insert into config(ip,config,md5) values (?,?,?)",(device,config_and_md5[0],config_and_md5[1]))
            conn.commit()
        else:
            if config_and_md5[1] != md5_result[0][2]:
                cursor.execute("update config set config=?,md5=? where ip=?",(config_and_md5[0],config_and_md5[1],device))
                conn.commit()
            else:
                continue
    cursor.execute('select * from config ')
    all_result = cursor.fetchall()
    for x in all_result:
        print(x[0],x[2])
    conn.close()





if __name__ == '__main__':
    # if os.path.exists('homeworkdb.sqlite'):
    #     os.remove('homeworkdb.sqlite')
    conn = sqlite3.connect('homeworkdb.sqlite')
    cursor = conn.cursor()

    # cursor.execute('create table config(ip varchar(40),config varchar(99999),md5 config varchar(999))')
    # conn.commit()
    # conn.close()

    write_config_md5_to_db()