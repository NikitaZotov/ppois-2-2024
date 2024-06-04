# Лабораторная номер 1.Вариант 69

### Модель подготовки к сдаче курсового проекта 69

### Предметная область: выполнение курсовых работ в рамках образовательного процесса.

### Важные сущности: курсовой проект, студент, руководитель проекта, исследование, дедлайны.

### Операции: ооперация выбора темы и планирования работы, перация сбора и анализа информации, операция написания и форматирования текста, операция консультаций с руководителем, операция сдачи проекта.

## Содержание лабораторной работы
### Лабораторная работа представляет из себя 5 классов: Teacher,Student,Person,CourseProject,Aplication.Класс студента наследуется от класса персоны,наследуя его поля такие как отправка сообщений и поля имени и фамилии.Класс учителя отвечает за выставление оценки студенту и выставления дедлайна.Класс курсовой проект отвечает за взаимосвязь между преподователем и учеником.В данной лабораторной работе были соблюдены такие принципы SOLID как S-single responsability,O-open\closed,L-Liskov Substitution.Из принципов ООП - наследование,полиморфизм,абстракция. 

## Реализация классов:
Класс Aplication:
```python
class Application:
    projects_info = {
        "Creating voice assistants and speech recognition applications.":
        """
            Designing applications that enable users to interact
            with devices using voice commands and incorporate speech recognition
            technology for improved user experience.
        """,
        "Creating applications for the analysis and forecasting of financial markets.":
        """
            Developing software tools for analyzing
            historical financial data, identifying patterns, and forecasting
            future market trends to aid investors and financial professionals
            in making informed decisions.
            """,
        "The use of artificial intelligence in medical diagnostics.":
        """
            Exploring the application of artificial intelligence techniques,
            such as machine learning and deep learning algorithms, to analyze
            medical imaging data and assist healthcare professionals in diagnosing
            diseases and conditions.
        """,
        "Development of companion robots for the elderly.":
        """
            Creating robotic companions designed to provide assistance
            and companionship to elderly individuals, offering features
            such as medication reminders, monitoring vital signs, and engaging
            in social interaction to improve overall well-being.
        """,
        "Creating applications for logistics and delivery management.":
        """
            Building software solutions to optimize the management of
            logistics operations, including inventory management, route
            optimization, and real-time tracking of shipments, to streamline
            the process of goods delivery and enhance efficiency.
        """
        }

    def __init__(self):
        self.teacher = None
        self.student = None
        self.actions = {
            "1": self.create_student,
            "2": self.create_teacher,
            "3": self.create_course_project,
            "4": self.check_deadline,
            "5": self.plan_project,
            "6": self.view_project_plan,
            "7": self.edit_project_info,
            "8": self.send_message_to_student,
            "9": self.send_message_to_teacher,
            "10": self.read_student_messages,
            "11": self.read_teacher_messages,
            "12": self.view_project_info,
            "13": self.grade_project, 
            "14": self.submit_project, 
            "15": exit
        }

    def display_menu(self):
        print("Выберите действие:")
        print("1. Создать студента")
        print("2. Создать учителя")
        print("3. Создать курсовой проект")
        print("4. Проверить дедлайн")
        print("5. Создать план курсового проекта")
        print("6. Просмотреть план курсового проекта")
        print("7. Сбор информации")
        print("8. Отправить сообщение студенту")
        print("9. Отправить сообщение учителю")
        print("10. Прочитать сообщения студента")
        print("11. Прочитать сообщения учителя")
        print("12. Просмотреть информацию о курсовом проекте")
        print("13. Выставить оценку за проект")  
        print("14. Сдать проект")  
        print("15. Выйти")


    
    def run(self):
        while True:
            self.display_menu()
            choice = input("Введите номер действия: ")
            if choice in self.actions:
                self.actions[choice]()
            elif choice.isdigit() and 1 <= int(choice) <= 15:
                print("Неверный выбор. Попробуйте снова.")
            else:
                print("Некорректный ввод. Пожалуйста, введите число от 1 до 15.")

    def view_project_info(self):
        if hasattr(self, 'student'):
            if hasattr(self.student, 'course_project') and hasattr(self.student,'project_info'):
                project_name = self.student.course_project
                project_info = self.projects_info.get(project_name)
                if project_info:
                    print(f"Информация о курсовом проекте '{project_name}':")
                    print(self.student.project_info)
                else:
                    print("Ошибка: Информация о выбранном курсовом проекте не найдена.")
            else:
                print("Ошибка: У студента нет курсового проекта/он пустой.")
        else:
            print("Студент не создан.")
            
    def edit_project_info(self):
        if hasattr(self, 'student'):
            project_name = self.student.course_project.strip()
            project_info = self.projects_info.get(project_name)
            if project_info:
                print(f"Интернет ресурс  на тему '{self.student.course_project[:-2]}':")
                print(project_info)
                while True:
                    project_info = input("Перепишите информацию: ")
                    if project_info.strip():  
                        self.student.project_info = project_info
                        break
                    else:
                        print("Ошибка: Информация не может быть пустой. Пожалуйста, введите информацию снова.")
                        project_info = input("Перепишите информацию: ")
                print("Информация о курсовом проекте успешно обновлена.") 
            else:
                print("Ошибка: Информация о выбранном курсовом проекте не найдена.")
        else:
            print("Студент не создан.")

    def view_project_plan(self):
        if hasattr(self, 'student') and hasattr(self.student, 'project_plan'):
            print("План работы над курсовым проектом:")
            print(self.student.project_plan.strip())
        else:
            print("План работы над курсовым проектом еще не составлен или студент не создан.")

    def create_student(self):
        
        first_name = input("Введите имя студента: ")
        while not first_name.strip():
            print("Пожалуйста, введите непустое имя.")
            first_name = input("Введите имя: ")
        last_name = input("Введите фамилию студента: ")
        while not last_name.strip():
            print("Пожалуйста, введите непустую строку.")
            last_name = input("Введите фамилию: ")
        group = input("Введите номер группы студента: ")
        while not group.strip():
            print("Пожалуйста, введите непустую строку.")
            group = input("Введите группу: ")
        self.student = Student(first_name, last_name, group)

    def grade_project(self):
        if hasattr(self, 'teacher') and hasattr(self, 'student'):
            if self.student.project_submitted:
                score = input("Введите оценку за проект: ")
                self.teacher.grade_project(self.student, int(score))
            else:
                print("Студент еще не сдал проект.")
        else:
            print("Для выставления оценки необходимо создать учителя и студента.")
        

    def submit_project(self):
        if hasattr(self, 'student') and hasattr(self, 'teacher'):
            if self.student.project_submitted:
                print("Проект уже был сдан.")
                return
            if self.student.course_project:
                if self.course_project.check_deadline():
                    print("Проект успешно отправлен учителю.")
                    self.student.project_submitted = True
                else:
                    print("Проект сдан после дедлайна. Оценка будет уменьшена на один балл.")
                    self.student.project_submitted = True
                    self.teacher.grade_project(self.student, -1)  
            else:
                print("Проект не был создан.")
        else:
            print("Для сдачи проекта необходимо создать студента и учителя.")

    def plan_project(self):
        if hasattr(self, 'student'):
            print("Планирование работы над курсовым проектом.")
            if hasattr(self.student, 'project_plan'):
                print("Текущий план работы:")
                print(self.student.project_plan.strip())
            print("Введите дополнительные этапы плана работы над курсовым проектом:")
            additional_steps = input("Дополнительные этапы: ")
            while not additional_steps.strip():
                print("Введите дополнительные этапы плана работы над курсовым проектом(не пустую строку):")
                additional_steps = input("Дополнительные этапы: ")
            if hasattr(self.student, 'project_plan'):
                self.student.project_plan += "\n" + additional_steps
            else:
                self.student.project_plan = additional_steps
            print("План работы над курсовым проектом обновлен:")
            print(self.student.project_plan.strip())
        else:
            print("Для составления плана проекта необходимо сначала создать студента.")
        return self.student.project_plan.strip()

    def create_teacher(self):
        is_teacher = True
        first_name = input("Введите имя учителя: ")
        while not first_name.strip():
            print("Пожалуйста, введите непустую строку.")
            first_name = input("Введите имя учителя: ")
        last_name = input("Введите фамилию учителя: ")
        while not last_name.strip():
            print("Пожалуйста, введите непустую строку.")
            last_name = input("Введите фамилию учителя: ")
        self.teacher = Teacher(first_name, last_name, is_teacher)

    def create_course_project(self):
        if hasattr(self, 'student') and hasattr(self, 'teacher'):
            self.course_project = CourseProject(self.student, self.teacher)
            print("Курсовой проект успешно создан.")
        else:
            print("Для создания курсового проекта необходимо сначала создать студента и учителя.")

    def check_deadline(self):
        if hasattr(self, 'course_project'):
            self.course_project.check_deadline()
        else:
            print("Курсовой проект еще не создан.")
            
    def send_message_to_teacher(self):
        if hasattr(self, 'student') and hasattr(self, 'teacher'):
            message = input("Введите сообщение для учителя: ")
            while not message.strip():
                message = input("Введите сообщение для учителя корректно: ")
            self.teacher.receive_message(message, self.student)
            print("Сообщение успешно отправлено учителю.")
        else:
            print("Для отправки сообщения необходимо сначала создать студента и учителя.")

    def send_message_to_student(self):
        if hasattr(self, 'student') and hasattr(self, 'teacher'):
            message = input("Введите сообщение для студента: ")
            while not message.strip():
                message = input("Введите сообщение для студента корректно: ")
            self.student.receive_message(message, self.teacher)
            print("Сообщение успешно отправлено студенту.")
        else:
            print("Для отправки сообщения необходимо сначала создать студента и учителя.")

    def read_student_messages(self):
        if hasattr(self, 'student'):
            if self.student.messages:
                print("Сообщения для студента:")
                for message in self.student.messages:
                    print(message)
            else:
                print("У студента пока нет сообщений.")
        else:
            print("Студент еще не создан.")

    def read_teacher_messages(self):
        if hasattr(self, 'teacher'):
            if self.teacher.messages:
                print("Сообщения для учителя:")
                for message in self.teacher.messages:
                    print(message)
            else:
                print("У учителя пока нет сообщений.")
        else:
            print("Учитель еще не создан.")
```

Класс CourseProject:
```python

class CourseProject:
    def __init__(self, student, teacher):

        if isinstance(student, Student) and isinstance(teacher, Teacher):
            self.student = student
            self.teacher = teacher
            self.group = self.student.group
            self.deadline = teacher.set_deadline(self.student.group)
        else:
            print("Вы передали обьекты не тех классов!")

    def check_deadline(self):
        deadline_str = self.deadline
        try:
            current_time = datetime.datetime.now()
            if current_time >= self.deadline:
                print(f"Дедлайн уже прошел. Он был {deadline_str}.")
                return False
            else:
                time_difference = self.deadline - current_time
                print(f"До дедлайна осталось {time_difference}.")
                return True
        except ValueError:
            print("Ошибка: неверный формат времени.")
            return False  

```

Класс Person:

```python
  class Person:
    def __init__(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name
        self.messages = []

    def receive_message(self, message, sender):
        if isinstance(sender, Teacher):
            self.messages.append(f"From {sender.first_name} {sender.last_name} (преподаватель): {message}")
        elif isinstance(sender, Student):
            self.messages.append(f"From {sender.first_name} {sender.last_name} ({sender.group}): {message}")
        else:
            self.messages.append(f"From {sender.first_name} {sender.last_name}: {message}")
```
Класс Sudent
```python
class Student(Person):

    def __init__(self, first_name: str, last_name: str, group: str):
        super().__init__(first_name, last_name)
        self.group = group
        self.course_project = self.get_course_project()
        self.project_submitted = False
        self.grade = 0

    def get_course_project(self):
        course_projects_list = [
            """Creating voice assistants and speech recognition applications.""",
            """Creating applications for the analysis and forecasting of financial markets.""",
            """The use of artificial intelligence in medical diagnostics.""",
            """Development of companion robots for the elderly.""",
            """Creating applications for logistics and delivery management.""",
        ]

        choice = input("Хотите выбрать тему сами (введите 'сам') или выбрать случайно (введите 'случайно')? ").lower()

        if choice == 'сам':
            print("Доступные темы:")
            for idx, topic in enumerate(course_projects_list, 1):
                print(f"{idx}. {topic}")

            topic_number = input("Выберите номер темы: ")
            while not topic_number.strip():
                topic_number =input("Выберите номер темы: ")
            topic_number = int(topic_number)
            if 1 <= topic_number <= len(course_projects_list):
                return course_projects_list[topic_number - 1]
            else:
                print("Ошибка: Неверный номер темы.")
                return None

        elif choice == 'случайно':
            return random.choice(course_projects_list)

        else:
            print("Ошибка: Неверный вариант выбора.")
            return None
    def submit_project(self, teacher):
        if self.project_submitted:
            print("Проект уже был сдан.")
            return
        if self.course_project:
            deadline = teacher.set_deadline(self.group)
            if self.course_project.check_deadline():
                print("Проект успешно отправлен учителю.")
                self.project_submitted = True
            else:
                print("Проект сдан после дедлайна. Оценка будет уменьшена на один балл.")
                self.project_submitted = True

        
        else:
            print("Проект не был создан.")
    

    def plan_project(self):
        print("Планирование работы над курсовым проектом.")
        print("Введите план работы над курсовым проектом (например, список этапов):")
        project_plan = input("План работы: ")
        return project_plan

    def get_course_project(self):
        course_projects_list = [
            """Creating voice assistants and speech recognition applications.""",
            """Creating applications for the analysis and forecasting of financial markets.""",
            """The use of artificial intelligence in medical diagnostics.""",
            """Development of companion robots for the elderly.""",
            """Creating applications for logistics and delivery management.""",
        ]
        
        choice = input("Хотите выбрать тему сами (введите 'сам') или выбрать случайно (введите 'случайно')? ").lower()
        while choice not in ["сам", "случайно"]:
            choice = input("Пожалуйста, введите 'сам' или 'случайно': ").lower()
        if choice == 'сам':
            print("Доступные темы:")
            for idx, topic in enumerate(course_projects_list, 1):
                print(f"{idx}. {topic}")

            topic_number = int(input("Выберите номер темы: "))
            if 1 <= topic_number <= len(course_projects_list):
                return course_projects_list[topic_number - 1]
            else:
                print("Ошибка: Неверный номер темы.")
                return None

        elif choice == 'случайно':
            return random.choice(course_projects_list)

        else:
            print("Ошибка: Неверный вариант выбора.")
            return None
```
Класс Teacher:
```python

class Teacher(Person):

    def __init__(self, first_name: str, last_name: str, is_teacher: bool = True):
        super().__init__(first_name, last_name)
        self.is_teacher = is_teacher

        
    def view_student_project_info(self, student):
        if student.course_project:
            project_name = student.course_project
            project_info = student.projects_info.get(project_name)
            if project_info:
                print(f"Информация о курсовом проекте студента {student.first_name} {student.last_name}:")
                print(project_info)
            else:
                print("Информация о курсовом проекте студента не найдена.")
        else:
            print("Студент еще не выбрал курсовой проект.")
            
    
    def grade_project(self, student, score):
        if student.project_submitted:
            if student.course_project:
                student.grade += score
                print(f"Оценка за проект студента {student.first_name} {student.last_name}: {student.grade}")
        else:
            print("Ошибка: Студент еще не сдал проект.")

    def set_deadline(self, group: str):
        while True:
            deadline = input(f"Введите время дедлайна для группы номер:{group} (ГГГГ-ММ-ДД ЧЧ:ММ): ")
            try:
                deadline = datetime.datetime.strptime(deadline, "%Y-%m-%d %H:%M")
                
                break
            except ValueError:
                print("Некорректный формат даты и времени. Пожалуйста, введите в формате ГГГГ-ММ-ДД ЧЧ:ММ.")
        return deadline
```
## Возможности интерфейса
![image](https://github.com/ellrckt/Studies/assets/117360867/699b6848-cea7-4d37-b0ed-48447209e393)

