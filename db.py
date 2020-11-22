#############################
# db.py
# mysql数据库读取和写入函数
#############################

# # 本地mysql
# import pymysql
#
# # user = input('请输入用户名：')
# # pwd = input('请输入密码：')
#
# # 1.连接
# conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='test', charset='utf8')


# 云端mysql
from sshtunnel import SSHTunnelForwarder
import pymysql
from str_sql import *

#通过SSH连接腾讯云服务器
server=SSHTunnelForwarder(
    ssh_address_or_host=('42.192.137.58',22),    #云服务器地址IP和端口port
    ssh_username='root',                         #云服务器登录账号admin
    ssh_password='Wa123456.',         #云服务器登录密码password
    remote_bind_address=('localhost',3306)       #数据库服务地址ip,一般为localhost和端口port，一般为3306
)
#云服务器开启
server.start()
#云服务器上mysql数据库连接
conn=pymysql.connect(host='127.0.0.1',             #此处必须是是127.0.0.1
                    port=server.local_bind_port,
                    user='root',                  #mysql的登录账号admin
                    password='Wa123456.',             #mysql的登录密码pwd
                    db='tc_management_db',                   #mysql中要访问的数据表
                    charset='utf8')               #表的字符集




# 2.创建游标
cursor = conn.cursor()

def password_verify(username, password):
    sql = "select student_password from student_info where student_id='%s' " % (username)
    cursor.execute(sql)
    result = cursor.fetchone()
    if result==None:
        return False
    else:
        if password == result[0]:
            # print(1)
            return True
        else:
            # print(0)
            return False


def get_data(sql, quantity=1):
    cursor.execute(sql)
    if quantity:
        return cursor.fetchone()
    else:
        return cursor.fetchall()
    # conn.close()


# 数据库写入数据
def write_data(sql):
    cursor.execute(sql)
    conn.commit()

if __name__ == '__main__':
    print(password_verify('2002','2002'))
