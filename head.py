from flask import Flask, render_template, request, flash, session, redirect, url_for
import time
# 导入wtf扩展的表单类
from flask_wtf import FlaskForm
# 导入自定义表单需要的字段
from wtforms import *
# 导入wtf扩展提供的表单验证器
from wtforms.validators import DataRequired, EqualTo
from db import *
import os


# 需要自定义一个表单类
class RegisterForm(FlaskForm):
    username = StringField('学号:', validators=[DataRequired()])
    password = PasswordField('密码:', validators=[DataRequired()])
    submit = SubmitField('登陆')


# 需要自定义一个表单类
class ChangePasswordForm(FlaskForm):
    # username = StringField('学号:', validators=[DataRequired()])
    password_old = PasswordField('原密码:', validators=[DataRequired()])
    password_new = PasswordField('新密码:', validators=[DataRequired()])
    password_new_2 = PasswordField('确认密码:', validators=[DataRequired(), EqualTo('password_new', '新密码输入不一致')])
    submit = SubmitField('提交')


# 定义一个选课表单类
class CourseForm(FlaskForm):
    course = StringField('课程:', validators=[DataRequired()])
    teacher = StringField('教师:', validators=[DataRequired()])
    submit = SubmitField('提交')


# 定义一个留言信息类
class MessageForm(FlaskForm):
    teacher = SelectField(
        label='教师',
        validators=[DataRequired('请选择标签')],
        render_kw={
            'class': 'form-control'
        },

        choices=[[111, ('高数', '李一', '女', '辅导员', '机电工程学院', '5.0')],
                 [114, ('机械工程材料', '李四', '女', '团委副书记', '管理学院', '4.5')]],
        # choices=[],
        default=1,
        coerce=int
    )
    # message = StringField('留言:', validators=[DataRequired()])
    message = TextAreaField('留言:', validators=[DataRequired()])
    submit = SubmitField('提交')


# 定义一个选课表单类
class EvaluateForm(FlaskForm):
    course = StringField('课程:', validators=[DataRequired()])
    teacher = StringField('教师:', validators=[DataRequired()])
    submit = SubmitField('提交')



# # 定义一个选课信息类
# class SelectForm(FlaskForm):
#     teacher = SelectField(
#         label='类别',
#         validators=[DataRequired('请选择标签')],
#         render_kw={
#             'class': 'form-control'
#         },
#
#         choices=[[111, ('高数', '李一', '女', '辅导员', '机电工程学院', '5.0')],
#                  [114, ('机械工程材料', '李四', '女', '团委副书记', '管理学院', '4.5')]],
#         # choices=[],
#         default=1,
#         coerce=int
#     )
#     # message = StringField('留言:', validators=[DataRequired()])
#     message = BooleanField('留言:', validators=[DataRequired()])
#     submit = SubmitField('提交')
