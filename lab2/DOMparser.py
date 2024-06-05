from xml.dom import minidom
from Student import Student


def add_note(file: str, student: Student):
    exam_titles, exam_grades = zip(*student.get_exams())
    exam_grades_string: str = ';'.join(str(exam_grades) for exam_grades in exam_grades)
    exam_titles_string: str = ';'.join(exam_titles)

    dom = minidom.parse(file)
    new_student = dom.createElement('student')

    name_element = dom.createElement('name')
    name_text = dom.createTextNode(student.get_name())
    name_element.appendChild(name_text)
    new_student.appendChild(name_element)

    group_element = dom.createElement('group')
    group_text = dom.createTextNode(str(student.get_group()))
    group_element.appendChild(group_text)
    new_student.appendChild(group_element)

    exam_title_element = dom.createElement('exam_title')
    exam_title_text = dom.createTextNode(exam_titles_string)
    exam_title_element.appendChild(exam_title_text)
    new_student.appendChild(exam_title_element)

    exam_grade_element = dom.createElement('exam_grade')
    exam_grade_text = dom.createTextNode(exam_grades_string)
    exam_grade_element.appendChild(exam_grade_text)
    new_student.appendChild(exam_grade_element)

    students_element = dom.getElementsByTagName('students')[0]
    students_element.appendChild(new_student)
    with open(file, 'w') as file:
        dom.writexml(file)


def delete_note_by_group(file: str, student_group: int) -> int:
    dom = minidom.parse(file)
    root = dom.documentElement
    student_elements = root.getElementsByTagName("student")

    counter: int = 0

    for student_element in student_elements:
        group_element = student_element.getElementsByTagName("group")[0]
        if group_element.firstChild.nodeValue == str(student_group):
            root.removeChild(student_element)
            counter += 1
    with open(file, 'w') as file:
        dom.writexml(file)
    return counter


def delete_note(file: str, name: str, group: int):
    dom = minidom.parse(file)
    root = dom.documentElement
    student_elements = root.getElementsByTagName("student")

    for student_element in student_elements:
        group_element = student_element.getElementsByTagName("group")[0]
        name_element = student_element.getElementsByTagName("name")[0]
        if group_element.firstChild.nodeValue == str(group) and name_element.firstChild.nodeValue == name:
            root.removeChild(student_element)

    with open(file, 'w') as file:
        dom.writexml(file)


