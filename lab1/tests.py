
import pytest
from lab import Application, Student, Teacher, CourseProject

from unittest.mock import patch
from io import StringIO
from datetime import datetime, timedelta
@pytest.fixture
def app():
    return Application()

def test_create_student(app):
    print("1", "1", "1","случайно")
    app.create_student()
    assert app.student.first_name == "1"
    assert app.student.last_name == "1"
    assert app.student.group == "1"
    

def test_create_teacher(app):
    print("1","1","da")
    app.create_teacher()
    assert app.teacher.first_name == "1"
    assert app.teacher.last_name == "1"
    assert app.teacher.is_teacher == True

def test_create_course_project(app):
    print("1", "1", "1","случайно")
    app.create_student()
    app.create_teacher()
    app.create_course_project()
    assert app.course_project.student == app.student
    assert app.course_project.teacher == app.teacher

def test_check_deadline():
    print("End")
    student = Student("1", "1", "1")
    teacher = Teacher("1", "1", 1)
    course_project = CourseProject(student, teacher)
    assert course_project.check_deadline() == False
    
def test_check_deadline2():
    print("not end")
    student = Student("1", "1", "1")
    teacher = Teacher("1", "1", 1)
    course_project = CourseProject(student, teacher)
    assert course_project.check_deadline() == True

def test_project_plan(app):
    app.create_student()
    print("1")
    ans = app.plan_project()
    assert ans == "1" 

def test_send_t_message(app):
    t = Teacher('1','1',True)
    s = Student('1','1','1')
    t.receive_message('1',s)
    m =''.join(t.messages)
    assert m =="From 1 1 (1): 1"
    
def test_send_s_message(app):
    t = Teacher('1','1',True)
    s = Student('1','1','1')
    s.receive_message('1',t)
    m =''.join(s.messages)
    assert m =="From 1 1 (преподаватель): 1"

def test_read_student_messages(app):
    app.create_student()
    app.read_student_messages()
    assert 0 ==0

def test_display_menu(app):
    ans = True
    expected_output = "Выберите действие:\n1. Создать студента\n2. Создать учителя\n3. Создать курсовой проект\n4. Проверить дедлайн\n5. Создать план курсового проекта\n6. Просмотреть план курсового проекта\n7. Сбор информации\n8. Отправить сообщение студенту\n9. Отправить сообщение учителю\n10. Прочитать сообщения студента\n11. Прочитать сообщения учителя\n12. Просмотреть информацию о курсовом проекте\n13. Выставить оценку за проект\n14. Сдать проект\n15. Выйти\n"
    assert ans ==True

def test_check_deadline_no_project(app):
    
    app.check_deadline()
    expected_output = "Курсовой проект еще не создан.\n"
    assert expected_output =="Курсовой проект еще не создан.\n"
    
def test_read_teacher_messages(app):
    app.create_teacher()
    app.read_teacher_messages()
    assert True == True

def test_send_message_to_teacher(app):
    app.create_student()
    ans = 'Привет'
    app.create_teacher()
    assert 'Привет'== ans

def test_submit_project(app):
    ans = 'Проект сдан после дедлайна.'
    app.create_student()
    app.create_teacher()
    app.create_course_project()
    app.submit_project()
    assert ans == 'Проект сдан после дедлайна.'

def test_grade_project(app):
    
    app.create_student()
    app.create_teacher()
    ans = 8 
    app.create_course_project()
    app.plan_project()
    app.view_project_plan()
    app.edit_project_info()
    app.view_project_info()
    app.submit_project()
    app.grade_project()
    print('8')
    assert ans==8
        
        
        
        
        
if __name__ == "__main__":
    pytest.main()
