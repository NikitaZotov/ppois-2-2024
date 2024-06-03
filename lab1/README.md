# Система управления университетом

## Введение
Данное программное обеспечение представляет собой модель университета, включающую различные классы для представления студентов, преподавателей, учебных планов, экзаменов, библиотеки и аудиторий. Оно позволяет управлять учебным процессом, зачислением студентов на курсы, организацией экзаменов и взаимодействием с библиотекой.

## Классы и методы

### Класс University
Класс, представляющий университет.

#### Методы

- `__init__(name: str, address: str) -> None`: Инициализирует объект класса University.
- `add_student(student: Student) -> None`: Добавляет студента в университет.
- `remove_student(student: Student) -> None`: Удаляет студента из университета.
- `add_professor(professor: Professor) -> None`: Добавляет преподавателя в университет.
- `add_curriculum(curriculum: Curriculum) -> None`: Добавляет учебный план в университет.
- `add_classroom(classroom: Classroom) -> None`: Добавляет аудиторию в университет.

### Класс Student
Класс, представляющий студентов.

#### Методы

- `__init__(first_name: str, last_name: str, age: int) -> None`: Инициализирует объект класса Student.
- `has_attended_all_lectures() -> bool`: Проверяет, посетил ли студент все лекции.
- `attend_lectures(subject: str, lectures_attended: int) -> None`: Посещает лекции.
- `enroll_to_curriculum(curriculum: Curriculum) -> None`: Зачисляет на учебный план.
- `borrow_book(library: Library) -> None`: Занимает книгу из библиотеки.
- `return_book(library: Library) -> None`: Возвращает книгу в библиотеку.
- `receive_stipend() -> None`: Получает стипендию.
- `has_completed_curriculum() -> bool`: Проверяет, завершил ли студент учебный план.
- `reset_curriculum() -> None`: Сбрасывает учебный план.

### Класс Professor
Класс, представляющий преподавателей.

#### Методы

- `__init__(first_name: str, last_name: str, age: int) -> None`: Инициализирует объект класса Professor.

### Класс Curriculum
Класс, представляющий учебные планы.

#### Методы

- `__init__(name: str, subjects: List[str], professors: Dict[str, Professor], lectures_per_subject: int = 10) -> None`: Инициализирует объект класса Curriculum.
- `display_curriculum_info() -> None`: Выводит информацию об учебном плане.

### Класс Classroom
Класс, представляющий аудитории.

#### Методы

- `__init__(number: str) -> None`: Инициализирует объект класса Classroom.

### Класс Library
Класс, представляющий библиотеку.

#### Методы

- `__init__(): -> None`: Инициализирует объект класса Library.
- `add_book(book_title, quantity) -> None`: Добавляет книгу в библиотеку.
- `display_available_books() -> List[str]`: Выводит доступные книги.
- `lend_book(book_title, borrower_name, borrower_last_name) -> None`: Выдает книгу студенту.
- `return_book(book_title, borrower_name, borrower_last_name) -> None`: Принимает возвращенную книгу.

### Класс Exam
Класс, представляющий экзамены.

#### Методы

- `__init__(subject: str, professor: str, classroom: str) -> None`: Инициализирует объект класса Exam.
- `take_exam(attendance: int, total_lectures: int) -> None`: Проходит экзамен.
- `display_exam_info() -> None`: Выводит информацию об экзамене.

### Класс Scholarship
Класс для расчета стипендии.

#### Методы

- `calculate_stipend(average_grade) -> int`: Рассчитывает стипендию на основе средней оценки.
