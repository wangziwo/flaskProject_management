def sql_qu_score(student_id):
    sql = '''  
    SELECT
        # student_info.student_name,
        # student_info.student_id,
        
        course_info.course_name,
        student_score.student_score
    FROM
     (student_info
     INNER JOIN
     student_exam
     ON
     student_info.student_id = student_exam.student_id
     INNER JOIN
     student_score
     ON
     student_info.student_id = student_score.student_id
     INNER JOIN
     exam_info
     ON
     student_exam.exam_id = exam_info.exam_id
     INNER JOIN
     course_info
     ON
     exam_info.course_id = course_info.course_id AND
     student_score.course_id = course_info.course_id)
    where
    student_info.student_id = 'rp_student_id'
    '''
    return sql.replace('rp_student_id', student_id)


def sql_qu_exam(student_id):
    sql = '''
    SELECT
        # student_exam.student_id, 
        course_info.course_name, 
        exam_info.exam_venue, 
        exam_info.exam_time, 
        course_info.course_credit
    FROM
        exam_info
        INNER JOIN
        student_exam
        ON 
            exam_info.exam_id = student_exam.exam_id
        INNER JOIN
        course_info
        ON 
            exam_info.course_id = course_info.course_id
    where
        student_exam.student_id = 'rp_student_id'
        '''
    return sql.replace('rp_student_id', student_id)

# 查询教师和课程对应语句，用于评教信息获取
def sql_qu_course_teacher_info(student_id):
    sql = '''
        SELECT
        # class_info.student_id, 
        course_info.course_name, 
        teacher_info.teacher_name, 
        teacher_info.teacher_sex, 
        teacher_info.teacher_Titles, 
        teacher_info.teacher_pro, 
        course_info.course_credit
    FROM
        class_info
        INNER JOIN
        course_info
        ON 
            class_info.course_id = course_info.course_id
        INNER JOIN
        teacher_info
        ON 
            class_info.teacher_id = teacher_info.teacher_id
    where
        class_info.student_id = 'rp_student_id'
        '''
    return sql.replace('rp_student_id', student_id)