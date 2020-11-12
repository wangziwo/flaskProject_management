def sql_qu_score(student_id):
    sql_qu_score = '''  
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
    return sql_qu_score.replace('rp_student_id',student_id)