from flask import Flask, render_template, request, flash, session, redirect, url_for

# 导入wtf扩展的表单类
from flask_wtf import FlaskForm
# 导入自定义表单需要的字段
from wtforms import SubmitField, StringField, PasswordField
# 导入wtf扩展提供的表单验证器
from wtforms.validators import DataRequired, EqualTo
from db import *
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
# # 更改代码立刻显示更新
# app.DEBUG = True
# # 更改模板立刻显示更新
app.jinja_env.auto_reload = True


# 解决编码问题
# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")


# 定义变量
global user


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
@app.route('/login', methods=['GET', 'POST'])
def log_in():
    register_form = RegisterForm()
    # return 'success!'
    # print(url_for(menu))
    if request.method == 'POST':

        # 调用validate_on_submit方法, 可以一次性执行完所有的验证函数的逻辑
        if register_form.validate_on_submit():

            # 进入这里就表示所有的逻辑都验证成功
            username = request.form.get('username')
            password = request.form.get('password')
            if password_verify(username=username, password=password) == True:
                # return 'success'
                session['username'] = username
                print(session.get('username'))
                # print(url_for(menu))
                # user = session['username']
                # return render_template("manu.html")
                return redirect(url_for('menu'))
            else:
                flash('密码错误')
        else:
            flash('参数有误')
    return render_template('login.html', form=register_form)


# 主页
@app.route('/')
def menu():
    # stu_info_url = url_for(stu_info)
    # print(stu_info_url)
    return render_template("manu2.html")
    # return render_template("manu.html")
# TODO 右上角显示

# # 主页
# @app.route('/')
# def menu():
#     return redirect(url_for('menu'))

# 学生信息页面
@app.route('/stu_info')
def stu_info():
    stu_id = session.get('username')
    info = get_data("select * from student_info where student_id ='%s'" % stu_id)
    print(info)
    if session.get('username'):

        return render_template('stu_info.html', info=info)
    else:
        return '请登录'


# 评教页面

# 定义一个选课表单类
class EvaluateForm(FlaskForm):
    course = StringField('课程:', validators=[DataRequired()])
    teacher = StringField('教师:', validators=[DataRequired()])
    submit = SubmitField('提交')


@app.route('/evaluate', methods=['GET', 'POST'])
def evaluate():
    if session.get('username'):
        stu_id = session.get('username')
        course_teacher_info = get_data(sql_qu_course_teacher_info(stu_id), 0)
        infu_num = len(course_teacher_info)
        sql = "select * from evaluate_info where student_id = '%s'" % stu_id
        print(get_data(sql), type(get_data(sql)))
        if get_data(sql):
            return '已经评教'
        # 获取输入框内容

        if request.method == 'POST':
            formdict = request.form.to_dict()
            print(formdict)
            for f in formdict:
                class_id = course_teacher_info[int(f)][0]
                # print(class_id)
                # print(f,formdict[f],type(f))
                # print(formdict)
                write_data(sql_evaluate_score_write(stu_id, class_id, formdict[f]))
                # sql = "select * from evaluate_info where student_id = '%s'" % stu_id
                # print(get_data(sql),len(get_data(sql)))
                return '已经评教'
        return render_template('evaluate.html', course_teacher_info=course_teacher_info,infu_num=infu_num)
    else:
        return redirect(url_for('log_in'))



# 考试信息页面
@app.route('/exam_info', methods=['GET', 'POST'])
def exam_info():
    if session.get('username'):
        stu_id = session.get('username')
        exam = get_data(sql_qu_exam(stu_id), 0)
        return render_template('exam_info.html', exam=exam)
    else:
        return redirect(url_for('log_in'))

# TODO 网页出错跳转提醒

# 登陆验证
@app.before_request
def is_login():
    if request.path == '/login':
        # print(request.path)
        return None
    else:
        if session.get('username'):
            # print(session.get('username'))
            return None
        else:
            return redirect(url_for('log_in'))


# 注销登陆
@app.route('/logout')
def logout():
    # 清空session
    session.clear()
    return redirect(url_for('log_in'))
# 成绩查询
@app.route('/score')
def score():

    stu_id = session.get('username')
    score = get_data(sql_qu_score(stu_id),0)
    # print(info)
    if session.get('username'):
        return render_template('stu_score.html', score=score)
    else:
        return redirect(url_for('log_in'))
# TODO 添加查询对应课程名称



if __name__ == '__main__':
    app.run()
