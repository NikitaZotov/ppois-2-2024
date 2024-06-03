# Лабораторная работа №1
**Цель**: 
- Изучить основные возможности языка Python для разработки программных систем с интерфейсом командной строки (CLI)
- Разработать программную систему на языке Python согласно описанию предметной области

**Задача**:

**Модель виртуальной кафедры 5**

**Предметная область**: организация обучения в виртуальной среде.

**Важные сущности**: виртуальная кафедра, студент, преподаватель, учебные материалы, задания, тесты, форум, онлайн-лекции.

**Операции**: операция доступа к учебным материалам, операция выполнения заданий, операция обсуждения на форуме, операция проведения онлайн-лекций, операция проведения тестирования.

<hr>

### Класс **VirtualDepartment**
Представляет собой виртуальную кафедру, предназначенный для хранения всех данных с ней связанных
#### Свойства:
- `name: str` - название кафедры
- `students: Dict[int, Student]` - словарь id студента - студент
- `teachers: Dict[int, Teacher]` - словарь id преподавателя - преподаватель
- `learning_materials: List[LearningMaterial]` - список учебных материалов
- `assignments: List[Assignment]` - список заданий
- `tests: List[Test]` - список тесов
- `forum: Forum` - форум кафедры
- `online_lectures: List[OnlineLecture]` - список проведенных онлайн-лекции

#### Методы:
- `add_student(self, student: 'Student') -> None` - добавляет студента на кафедру
- `remove_student(self, student_id: int) -> None` - удаляет студента с кафедры
- `add_teacher(self, teacher: 'Teacher') -> None` - добавляет преподавателя на кафедру
- `remove_teacher(self, teacher_id: int) -> None` - удаляет преподавателя с кафедры
- `add_learning_material(self, material: 'LearningMaterial') -> None` - добавляет учебный материал на кафедру
- `remove_learning_material(self, title: str) -> None` - удаляет учебный материал с кафедры
- `add_assignment(self, assignment: 'Assignment') -> None` - добавляет задание на кафедру
- `remove_assignment(self, title: str) -> None` - удаляет задание с кафедры
- `add_test(self, test: 'Test') -> None` - добавляет тест на кафедру
- `remove_test(self, title: str) -> None` - удаляет тест с кафедры
- `conduct_online_lecture(self, lecture: 'OnlineLecture') -> None` - проведение онлайн-лекции
- `view_completed_lectures(self) -> List[Tuple[str, str, List[str]]]` - возвращает список с информацией(преподаватель, тема, присутствующие) о проведенных онлайн-лекциях
- `view_available_tests(self) -> List[str]` - возвращает список с названиями доступных тестов
- `view_available_assignments(self) -> List[str]` - возвращает список с названиями доступных заданий
- `view_learning_materials(self) -> List[str]` - возвращает список с названиями доступных учебных материалов

Выбрасывает исключения: **ValueError**

<hr>

### Класс **User**
Представляет собой пользователья
#### Свойства
- `id: int` - id
- `full_name: str` - имя

#### Методы
- `check_id(id: int) -> int` - проверяет а корректоность id(целое положительное число)

Выбрасывает исключения: **ValueError**

<hr>

### Класс **Student(User)**
Представляет собой студента
#### Свойства
- наследуемые от класса `User`
- `department: VirtualDepartment` - кафедра обучения
- `completed_assignments: List[str]` - список с названиями выполненных заданий
- `completed_tests: Dict[str, Any]` - словарь с названиями выполненных тестов и ответами на них
#### Методы
- `__init__(self, id: int, full_name: str, department: VirtualDepartment)` - создание студента с указанными свойствами
- `complete_assignment(self, assignment_title: str, submission: Any) -> None` - попытка выполнить задание
- `complete_test(self, test_title: str, answers: Any) -> None` - попытка выполнить тест
- `view_completed_assignments(self) -> List[str]` - возвращает список с названиями выполненных заданий
- `view_completed_tests(self) -> List[str]` - возвращает список с названиями выполненных тестов

Выбрасывает исключения: **ValueError**

<hr>

### Класс **Teacher(User)**
Представляет собой преподавателя
#### Свойства
- наследуемые от класса `User`

#### Методы
- `__init__(self, id: int, full_name: str)` - создание преподавателя с указанными текстом и датой
- `create_assignment(self, title: str, description: str) -> 'Assignment'` - возвращает созданное преподавателем задание
- `create_test(self, title: str, questions: List[str]) -> 'Test'` - возвращает созданный преподавателем тест
- `conduct_online_lecture(self, topic: str, students_present: List[Student]) -> 'OnlineLecture'` - возвращает созданную преподавателем онлайн-лекцию

<hr>

### Класс **LearningMaterial**
Представляет собой учебный материал
#### Свойства
- `title: str` - заголовок
- `content: str` - содержание

<hr>

### Класс **Assignment**
Представляет собой задание
#### Свойства
- `title: str` - заголовок
- `content: str` - описание
- `submissions: Dict[int, Any]` - словарь с id выполнивших задание студентов и их ответами

#### Методы
- `submit(self, student: Student, submission: Any) -> None` - добавление в `submissions` ответа студента по ключу id

<hr>

### Класс **Test**
Представляет собой тест
#### Свойства
- `title: str` - заголовок
- `questions: List[str]` - список вопросов
- `submissions: Dict[int, Any]` - словарь с id прошедших тест студентов и их ответами

#### Методы
- `submit(self, student: Student, answers: Any) -> None` - добавление в `submissions` ответа студента по ключу id

<hr>

### Класс **Forum**
Представляет собой форум
#### Свойства
- `threads: List[ForumThread]` - список тем

#### Методы
- `create_thread(self, author: User, title: str, content: str) -> None` - создание тему с указанными параметрами
- `add_post(self, thread_title: str, author: User, content: str) -> None` - добавляет пост с указанными параметрами в указанную тему
- `view_all_threads(self) -> List[Tuple[str, str]]` - возвращает список всех тем
- `view_thread_posts(self, thread_title: str) -> List[Tuple[str, str]]` - возвращает список всех постов из указанной темы

Выбрасывает исключения: **ValueError**

<hr>

### Класс **ForumThread**
Представляет собой тему на форуме
#### Свойства
- `author: User` - автор темы 
- `title: str` - заголовок
- `content: str` - содержание темы
- `posts: List[ForumPost]` - посты-ответы по теме

#### Методы
- `add_post(self, author: User, content: str) -> None` - добавляет пост с указанными параметрами в тему

<hr>

### Класс **ForumPost**
Представляет собой пост на форуме
#### Свойства
- `author: User` - автор поста
- `content: str` - содержание поста

<hr>

### Класс **OnlineLecture**
Представляет собой онлайн-лекцию
#### Свойства
- `teacher: Teacher` - преподаватель, проводящий онлайн-лекцию
- `topic: str` - тема онлайн-лекции
- `students_present: List[Student]` - список присутствующих на лекции студентов

