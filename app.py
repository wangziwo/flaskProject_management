from head import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'os.urandom(24)'

# app.DEBUG = True
# # 更改模板立刻显示更新
app.jinja_env.auto_reload = True

# 定义变量
global user


# 登陆界面
@app.route('/login', methods=['GET', 'POST'])
def log_in():
    register_form = RegisterForm()
    if request.method == 'POST':
        # 调用validate_on_submit方法, 可以一次性执行完所有的验证函数的逻辑
        if register_form.validate_on_submit():
            # 进入这里就表示所有的逻辑都验证成功
            username = request.form.get('username')
            password = request.form.get('password')
            if password_verify(username=username, password=password) == True:
                session['username'] = username
                print(session.get('username'))
                return redirect(url_for('menu'))
            else:
                flash('账号或密码错误')
        else:
            flash('参数有误')
    return render_template('login.html', form=register_form)


# 主页
@app.route('/')
def menu():
    stu_id = session.get('username')
    sql = "select student_name from student_info where student_id = '%s'" % stu_id
    stu_name = get_data(sql)
    return render_template("manu2.html", user_id=stu_id, user_name=stu_name[0])


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
                write_data(sql_evaluate_score_write(stu_id, class_id, formdict[f]))
            return '已经评教'
        return render_template('evaluate.html', course_teacher_info=course_teacher_info, infu_num=infu_num,
                               option=list(range(10, 0, -1)))
    else:
        return redirect(url_for('log_in'))


# 学生留言
@app.route('/message', methods=['GET', 'POST'])
def message():
    if session.get('username'):
        message_form = MessageForm()
        stu_id = session.get('username')
        course_teacher_info = get_data(sql_message_teacher_info(stu_id), 0)
        info_num = len(course_teacher_info)
        # 转为列表
        ls_course_teacher_info = []
        for cour in course_teacher_info:
            l1 = cour[0]
            l2 = cour[1:]
            ls = [l1, l2]
            ls_course_teacher_info.append(ls)
        message_form.teacher.choices = ls_course_teacher_info

        # 获取输入框内容
        if request.method == 'POST':
            class_id = request.form.get('teacher')
            message_info = request.form.get('message')
            print(class_id, message_info)
            sql = '''insert into message_info (student_id, class_id, message) 
                       VALUES ("%s","%s","%s")''' % (stu_id, class_id, message_info)
            print(sql)
            write_data(sql)
            return '留言成功！'
        return render_template('message.html', course_teacher_info=course_teacher_info, info_num=info_num,
                               form=message_form)
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


# 登陆验证
@app.before_request
def is_login():
    if request.path == '/login':
        return None
    else:
        if session.get('username'):
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
    score = get_data(sql_qu_score(stu_id), 0)
    if session.get('username'):
        return render_template('stu_score.html', score=score)
    else:
        return redirect(url_for('log_in'))


# 密码修改
@app.route('/change_pd', methods=['GET', 'POST'])
def change_pd():
    change_password_form = ChangePasswordForm()
    if request.method == 'POST':

        # 调用validate_on_submit方法, 可以一次性执行完所有的验证函数的逻辑
        if change_password_form.validate_on_submit():

            # 进入这里就表示所有的逻辑都验证成功
            student_id = session.get('username')
            password_old = request.form.get('password_old')
            new_password = request.form.get('password_new')
            if password_verify(student_id, password_old):
                sql = "update student_info set student_password = '%s' where student_id = '%s'" % (
                    new_password, student_id)
                write_data(sql)
                print(session.get('username'))
                flash('密码修改成功,下次登陆需要使用新密码')

            else:
                flash('原密码错误，请重新输入！')
        else:
            flash('两次密码不一样！')
    return render_template('change_pd.html', form=change_password_form)


# 课程正选
@app.route('/select', methods=['GET', 'POST'])
def select():
    if session.get('username'):
        stu_id = session.get('username')
        course_info = get_data("select * from course_info", 0)
        info_num = len(course_info)
        # 转为列表
        ls_course_info = []
        for cour in course_info:
            l1 = cour[0]
            l2 = cour[1:]
            ls = [l1, l2]
            ls_course_info.append(ls)
        print(course_info)
        if request.method == 'POST':
            select_list = request.form.getlist('select_info')
            print("select_list:", select_list)
            for se in select_list:
                write_data("insert into class_info (student_id,course_id) values ('%s','%s')" % (stu_id, se))
            return '选课成功'
        return render_template('select.html', course_info=course_info)
    else:
        return redirect(url_for('log_in'))


# 查询选课结果
@app.route('/select_result')
def select_result():
    if session.get('username'):
        stu_id = session.get('username')
        result = get_data(sql_select_result(stu_id), 0)

        return render_template('select_result.html', result=result)
    else:
        return redirect(url_for('log_in'))


# 课程退选
@app.route('/deselect', methods=['GET', 'POST'])
def deselect():
    if session.get('username'):
        stu_id = session.get('username')
        result = get_data(sql_deselect_info(stu_id), 0)
        print(result)
        if request.method == 'POST':
            deselect_list = request.form.getlist('deselect_info')
            print("deselect_list:", deselect_list)
            for de in deselect_list:
                write_data("delete from class_info  where class_id  = '%s'" % (de))

            return '退选成功'
        return render_template('deselect.html', result=result)
    else:
        return redirect(url_for('log_in'))


# 课表显示
@app.route('/schedule')
def schedule():
    if session.get('username'):
        stu_id = session.get('username')
        schedule = get_data(sql_select_result(stu_id), 0)
        return render_template('schedule.html', schedule=schedule)
    else:
        return redirect(url_for('log_in'))


if __name__ == '__main__':
    app.run()
