import pymysql

# user = input('请输入用户名：')
# pwd = input('请输入密码：')

# 1.连接
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='test', charset='utf8')
# 2.创建游标
cursor = conn.cursor()


#
# #注意%s需要加引号
# # sql = "select * from t1.userinfo where username='%s' and pwd='%s'" %(user, pwd)
# username = '1'
# sql = "select name from stu where stu_id='%s'"%(username)
# print(sql)
#
# # 3.执行sql语句
# cursor.execute(sql)
#
# result=cursor.fetchone() #执行sql语句，返回sql查询成功的记录数目
# print(result[0],type(result[0]))
#
# # 关闭连接，游标和连接都要关闭
# cursor.close()
# conn.close()
#
# if result:
#     print('登陆成功')
# else:
#     print('登录失败')
# 密码验证函数
def password_verify(username, password):
    sql = "select name from stu where stu_id='%s'" % (username)
    cursor.execute(sql)
    result = cursor.fetchone()
    if password == result[0]:
        print(1)
        return True
    else:
        print(0)
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
    # password_verify(1,'wang')
    # print(get_data('select * from stu',0))
    write_data('insert into stu values ("2004","li","2004","软件182","软件工程")')