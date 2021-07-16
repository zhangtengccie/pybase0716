# import sqlite3
# #
# conn = sqlite3.connect('configuredb.sqlite')
# cursor = conn.cursor()
# cursor.execute('create table config(ip varchar(40),config varchar(99999),md5 config varchar(999))')

from ssh_router import ssh_cli
import hashlib
import re
import sqlite3

device_list = ['1.1.1.200']
username = 'cisco'
password = 'cisco'

def get_config_md5(ip,username,password):
    try:
        device_config = ssh_cli(ip, username, password)
        ret = re.split(r'\nhostname \S+\n', device_config)
        run_conf = re.findall('hostname.*',str(ret))
        m = hashlib.md5()
        m.update(str(run_conf).encode())
        md5_value = m.hexdigest()
        return run_conf,md5_value

    except Exception:
        return

def write_config_md5_to_db():

    conn = sqlite3.connect('configuredb.sqlite')
    cursor = conn.cursor()
    # cursor.execute('select * from config')
    # ret = cursor.fetchall()
    # for i in ret:
    #     print(i)
    for device in device_list:
        conn = sqlite3.connect('configuredb.sqlite')
        cursor = conn.cursor()
        config_and_md5 = get_config_md5(device,username,password)
        config_info = config_and_md5[0][0]
        md5_info = config_and_md5[1]
        cursor.execute('select * from config')
        md5_result = cursor.fetchall()
        if not md5_result:
            cursor.execute(f'insert into config(ip, config, md5) values("{device}","{config_info}","{md5_info}")')
            cursor.fetchall()
            conn.commit()
        else:
            cursor.execute(f'select md5 from config where ip = "{device}"')
            md5 = cursor.fetchall()
            md5 = md5[0][0]
            if md5 != md5_info:
                t = f"update config  set config=?,md5=? where ip = ?"
                cursor.execute(t,(config_info,md5_info,device))

            else:
                continue
    cursor.execute('select * from config')
    all_result = cursor.fetchall()
    for x in all_result:
        print(x[0],x[2])
    conn.commit()



if __name__ == '__main__':

    # ret =get_config_md5('1.1.1.200',username,password)
    write_config_md5_to_db()