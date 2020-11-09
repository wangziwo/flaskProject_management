from flask import Flask, render_template, request, flash
# 导入wtf扩展的表单类
from flask_wtf import FlaskForm
# 导入自定义表单需要的字段
from wtforms import SubmitField, StringField, PasswordField
# 导入wtf扩展提供的表单验证器
from wtforms.validators import DataRequired, EqualTo
from db import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'heima'
# 更改代码立刻显示更新
# app.DEBUG = True
# 更改模板立刻显示更新
app.jinja_env.auto_reload = True


# 解决编码问题
# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")

# 需要自定义一个表单类
class RegisterForm(FlaskForm):
    username = StringField('学号:', validators=[DataRequired()])
    password = PasswordField('密码:', validators=[DataRequired()])
    submit = SubmitField('登陆')


# 定义一个选课表单类
class CourseForm(FlaskForm):
    course = StringField('课程:', validators=[DataRequired()])
    teacher = StringField('教师:', validators=[DataRequired()])
    submit = SubmitField('提交')


# 登陆界面
@app.route('/', methods=['GET', 'POST'])
def log_in():
    register_form = RegisterForm()
    if request.method == 'POST':
        # 调用validate_on_submit方法, 可以一次性执行完所有的验证函数的逻辑
        if register_form.validate_on_submit():
            # 进入这里就表示所有的逻辑都验证成功
            username = request.form.get('username')
            password = request.form.get('password')
            if password_verify(username=username, password=password) == True:
                # return 'success'
                return render_template("manu.html")
            else:
                flash('密码错误')
        else:
            flash('参数有误')

    return render_template('login.html', form=register_form)


# 主页
@app.route('/<num>')
def get_hello_world(num):
    url_1 = 'www.baidu.com'
    my_list = [1, 3, 5, 9]
    return render_template('index.html',
                           url_1=url_1,
                           my_list=my_list
                           )


# 学生信息页面
@app.route('/id/<int:stu_id>')
def stu_info(stu_id):
    info = get_data("select * from stu where stu_id ='%s'" % stu_id)
    print(info)
    return render_template('content/templates/stu_info.html', info=info)


# 评教页面
@app.route('/id/<int:stu_id>/evaluate', methods=['GET', 'POST'])
def evaluete_teaching(stu_id):
    course_form = CourseForm()
    # write_data("insert into stu values ('2004','li','2004','软件182','软件工程'")
    return render_template('content/templates/course_selection.html', form=course_form)


if __name__ == '__main__':
    app.run()
