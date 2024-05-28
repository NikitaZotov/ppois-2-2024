import random

from files.Exam import Exam
from files.Professor import Professor
from files.Student import Student
from files.University import University
from files.Library import Library
from files.Curriculum import Curriculum
from files.Classroom import Classroom

# Создаем университет
university = University("БГУИР", "Гикало 9")

# Добавляем преподавателей
professor1 = Professor("Иван", "Иванов", 40)
professor2 = Professor("Пётр", "Петров", 35)
professor3 = Professor("Сергей", "Смирнов", 45)
professor4 = Professor("Алексей", "Алексеев", 50)
professor5 = Professor("Ольга", "Кузнецова", 38)
professor6 = Professor("Наталья", "Васильева", 42)
professor7 = Professor("Мария", "Петрова", 33)
professor8 = Professor("Владимир", "Михайлов", 48)
professor9 = Professor("Татьяна", "Фёдорова", 41)
professor10 = Professor("Екатерина", "Попова", 36)
university.add_professor(professor1)
university.add_professor(professor2)
university.add_professor(professor3)
university.add_professor(professor4)
university.add_professor(professor5)
university.add_professor(professor6)
university.add_professor(professor7)
university.add_professor(professor8)
university.add_professor(professor9)
university.add_professor(professor10)

# Добавляем студентов
student1 = Student("Лиза", "Киреева", 20)
student2 = Student("Настя", "Шомпол", 21)
student3 = Student("Павел", "Китель", 18)
student4 = Student("Иван", "Петров", 19)
university.add_student(student1)
university.add_student(student2)
university.add_student(student3)
university.add_student(student4)

# Создаем учебные планы
curriculum1 = Curriculum(
    "Компьютерные науки",
    [
        "Математика",
        "Программирование",
        "Структуры данных",
        "Алгоритмы",
        "Сетевые технологии",
    ],
    {
        "Математика": professor1,
        "Программирование": professor2,
        "Структуры данных": professor3,
        "Алгоритмы": professor4,
        "Сетевые технологии": professor5,
    },
    lectures_per_subject=10,  # Количество занятий за каждый предмет в семестре
)

curriculum2 = Curriculum(
    "Физика",
    [
        "Механика",
        "Термодинамика",
        "Электромагнетизм",
        "Квантовая физика",
        "Астрофизика",
    ],
    {
        "Механика": professor6,
        "Термодинамика": professor7,
        "Электромагнетизм": professor8,
        "Квантовая физика": professor9,
        "Астрофизика": professor10,
    },
    lectures_per_subject=20,  # Количество занятий за каждый предмет в семестре
)


# Добавляем учебные планы в университет
university.add_curriculum(curriculum1)
university.add_curriculum(curriculum2)

# Создаем библиотеку и добавляем в нее книги
library = Library()
library.add_book("Морфий", 0)
library.add_book("Государь", 3)
library.add_book("Введение в Python", 4)
library.add_book("Введение в Математический анализ", 6)
library.add_book("Стандарт OSTIS", 7)
library.add_book("Кулинарные шедевры", 1)

# Создаем аудитории
classroom1 = Classroom("101")
classroom2 = Classroom("102")
classroom3 = Classroom("103")
classroom4 = Classroom("104")
classroom5 = Classroom("105")
classroom6 = Classroom("201")
classroom7 = Classroom("202")
classroom8 = Classroom("203")
classroom9 = Classroom("204")
classroom10 = Classroom("205")

# Добавляем аудитории в университет
university.add_classroom(classroom1)
university.add_classroom(classroom2)
university.add_classroom(classroom3)
university.add_classroom(classroom4)
university.add_classroom(classroom5)
university.add_classroom(classroom6)
university.add_classroom(classroom7)
university.add_classroom(classroom8)
university.add_classroom(classroom9)
university.add_classroom(classroom10)

while True:
    print("\nВыбор:")
    print("1. Зачислить студента в университет")
    print("2. Выбрать студента для взаимодействия")
    print("3. Выйти")
    choice = input("Выберите действие: ")

    if choice == "3":
        print("Программа остановлена.")
        break

    elif choice == "1":
        first_name = input("Введите имя студента: ")
        while not Student.validate_name(first_name):
            print(
                "Некорректное имя. Имя должно начинаться с заглавной буквы и содержать только буквы."
            )
            first_name = input("Введите имя студента: ")
        last_name = input("Введите фамилию студента: ")
        while not Student.validate_name(last_name):
            print(
                "Некорректная фамилия. Фамилия должна начинаться с заглавной буквы и содержать только буквы."
            )
            last_name = input("Введите фамилию студента: ")
        age = int(input("Введите возраст студента: "))
        while not Student.validate_age(age):
            print("Некорректный возраст. Возраст должен быть от 16 до 100.")
            age = int(input("Введите возраст студента: "))
        new_student = Student(first_name, last_name, age)
        university.add_student(new_student)

    elif choice == "2":
        if not university.students:
            print("Нет зарегистрированных студентов.")
            continue

        print("Список студентов:")
        for i, student in enumerate(university.students, start=1):
            print(f"{i}. {student.first_name} {student.last_name}")

        student_index = int(input("Выберите студента: ")) - 1
        if 0 <= student_index < len(university.students):
            selected_student = university.students[student_index]
            print(
                f"Выбран студент: {selected_student.first_name} {selected_student.last_name}"
            )

            while True:
                print("\nВыберите действие для студента:")
                print("1. Посетить библиотеку")
                print("2. Какие книги есть у студента")
                print("3. Учиться")
                print("4. Посмотреть баланс")
                print("5. Назад")
                action = input("Выберите действие: ")

                if action == "1":
                    while True:
                        print("\nВыберите действие в библиотеке:")
                        print("1. Взять книгу")
                        print("2. Сдать книгу")
                        print("3. Назад")
                        library_action = input("Выберите действие: ")

                        if library_action == "1":
                            selected_student.borrow_book(library)

                        elif library_action == "2":
                            selected_student.return_book(library)

                        elif library_action == "3":
                            break

                elif action == "2":
                    print(
                        f"Список книг студента {selected_student.first_name} {selected_student.last_name}:"
                    )
                    selected_student.display_student_books()

                elif action == "3":
                    while True:
                        print("\nВыберите действие:")
                        print("1. Выбрать учебный план")
                        print("2. Посетить учебные занятия")
                        print("3. Сдать экзамены")
                        print("4. Назад")
                        study_action = input("Выберите действие: ")

                        if study_action == "1":
                            if (
                                selected_student.curriculum
                                and not selected_student.has_completed_curriculum()
                            ):
                                print(
                                    "Вы не можете выбрать новый учебный план, пока не завершите текущий."
                                )
                                continue

                            print("Список доступных учебных планов:")
                            for i, curriculum in enumerate(
                                university.curriculums, start=1
                            ):
                                print(f"{i}. {curriculum.name}")
                            curriculum_index = int(input("Выберите учебный план: ")) - 1
                            if 0 <= curriculum_index < len(university.curriculums):
                                selected_curriculum = university.curriculums[
                                    curriculum_index
                                ]
                                print(f"Вы выбрали учебный план")
                                selected_curriculum.display_curriculum_info()
                                selected_student.enroll_to_curriculum(
                                    selected_curriculum
                                )

                        elif study_action == "2":
                            if selected_student.has_attended_all_lectures():
                                print(
                                    "Вы уже посетили учебные занятия. Повторное посещение невозможно."
                                )
                                continue
                            if selected_student.curriculum:
                                print("Посещение учебных занятий:")
                                for i, subject in enumerate(
                                    selected_student.curriculum.subjects, start=1
                                ):
                                    total_lectures = (
                                        selected_student.curriculum.lectures_per_subject
                                    )
                                    while True:
                                        try:
                                            lectures_attended = int(
                                                input(
                                                    f"Сколько занятий вы посетили по предмету '{subject}': "
                                                )
                                            )
                                            if 0 <= lectures_attended <= total_lectures:
                                                selected_student.attend_lectures(
                                                    subject, lectures_attended
                                                )
                                                break
                                            else:
                                                print(
                                                    f"Неверное количество занятий. Введите число от 0 до {total_lectures}."
                                                )
                                        except ValueError:
                                            print("Ошибка: введите целое число.")
                            else:
                                print("Сначала выберите учебный план.")

                        elif study_action == "3":
                            if not selected_student.curriculum:
                                print("Сначала выберите учебный план.")
                                continue

                            subjects_attended = (
                                selected_student.subjects_attendance.keys()
                            )
                            if len(subjects_attended) < len(
                                selected_student.curriculum.subjects
                            ):
                                print(
                                    "Вы не посетили все предметы своего учебного плана."
                                )
                                print(
                                    "Перейдите к пункту 2 и посетите учебные занятия."
                                )
                                continue

                            for subject in selected_student.curriculum.subjects:
                                professor = selected_student.curriculum.professors[
                                    subject
                                ]
                                classroom = random.choice(university.classrooms)

                                attendance = selected_student.subjects_attendance[
                                    subject
                                ]
                                total_lectures = (
                                    selected_student.curriculum.lectures_per_subject
                                )
                                exam = Exam(
                                    subject,
                                    f"{professor.first_name} {professor.last_name}",
                                    classroom,
                                )
                                exam.take_exam(attendance, total_lectures)
                                exam.display_exam_info()

                                selected_student.exams[subject] = exam

                            if all(
                                exam.passed for exam in selected_student.exams.values()
                            ):
                                total_grade = sum(
                                    selected_student.exams[subject].grade
                                    for subject in selected_student.curriculum.subjects
                                )
                                average_grade = total_grade / len(
                                    selected_student.curriculum.subjects
                                )
                                print("Все экзамены сданы!")
                                selected_student.receive_stipend()
                                selected_student.reset_curriculum()
                            else:
                                print("Не все экзамены сданы.")
                                for subject, exam in selected_student.exams.items():
                                    if not exam.passed:
                                        print(f"Предмет: {subject}")

                                choice = input(
                                    "1. Пересдать "
                                    "2. Отчисление: "
                                    "Выберите действие: "
                                )
                                if choice == "1":
                                    for subject, exam in selected_student.exams.items():
                                        if not exam.passed:
                                            exam.grade = random.randint(4, 6)
                                            exam.display_exam_info()
                                    selected_student.reset_curriculum()
                                elif choice == "2":
                                    university.remove_student(selected_student)
                                    exit()
                                else:
                                    print(
                                        "Выбрано некорректное действие. Попробуйте еще раз."
                                    )

                        elif study_action == "4":
                            break

                elif action == "4":
                    print("Баланс:", selected_student.balance)

                elif action == "5":
                    break
