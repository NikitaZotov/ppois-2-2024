import tkinter as tk
import xml.etree.ElementTree as ET
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
from controller.controller import Controller
from model.model import Storage

class MyApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.storage = Storage()
        self.controller = Controller(self.storage)
        self.current_page = 1
        self.max_page = 10
        self.max_students_per_page = 10
        self.up_st = None
        
        self.title("Таблица студентов")
        self.configure(bg='#fafafa')
        self.attributes('-alpha', 1)
        self.geometry("1000x500")

        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.top_frame = tk.Frame(self.main_frame, bg='#fafafa')
        self.top_frame.pack(side=tk.TOP, fill=tk.X)

        self.add_student_button = tk.Button(self.top_frame, text="Добавить студента", command=self.add_student)
        self.add_student_button.pack(side=tk.LEFT, padx=20, pady=20)

        self.search_button = tk.Button(self.top_frame, text="Поиск", command=self.search)
        self.search_button.pack(side=tk.LEFT, padx=20, pady=20)

        self.delete_button = tk.Button(self.top_frame, text="Удаление", command=self.delete)
        self.delete_button.pack(side=tk.LEFT, padx=20, pady=20)

        self.file_button = tk.Button(self.top_frame, text="Файловые операции", command=self.file_operations)
        self.file_button.pack(side=tk.LEFT, padx=20, pady=20)

        self.top_frame2 = tk.Frame(self.main_frame, bg='#fafafa')
        self.top_frame2.pack(side=tk.TOP, fill=tk.X)

        self.label_student = tk.Label(self.top_frame2, text="Имя студента", bg='#fafafa')
        self.label_student.pack(side=tk.LEFT, padx=5, pady=5)

        self.label_course = tk.Label(self.top_frame2, text="Курс", bg='#fafafa')
        self.label_course.pack(side=tk.LEFT, padx=5, pady=5)

        self.label_group = tk.Label(self.top_frame2, text="Группа", bg='#fafafa')
        self.label_group.pack(side=tk.LEFT, padx=5, pady=5)

        self.label_total_works = tk.Label(self.top_frame2, text="Всего работ", bg='#fafafa')
        self.label_total_works.pack(side=tk.LEFT, padx=5, pady=5)

        self.label_completed_works = tk.Label(self.top_frame2, text="Вып. работы", bg='#fafafa')
        self.label_completed_works.pack(side=tk.LEFT, padx=5, pady=5)

        self.label_programming_language = tk.Label(self.top_frame2, text="Язык прогр.", bg='#fafafa')
        self.label_programming_language.pack(side=tk.LEFT, padx=5, pady=5)

        self.table_frame = tk.Frame(self.main_frame, bg='#fafafa')
        self.table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.student_list = tk.Listbox(self.table_frame, width=40)
        self.student_list.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.bottom_frame = tk.Frame(self.main_frame, bg='#fafafa')
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.prev_page_button = tk.Button(self.bottom_frame, text="Предыдущая страница", command=self.prev_page)
        self.prev_page_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.page_label = tk.Label(self.bottom_frame, text="Страница 1", bg='#fafafa')
        self.page_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.next_page_button = tk.Button(self.bottom_frame, text="Следующая страница", command=self.next_page)
        self.next_page_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.max_page_label = tk.Label(self.bottom_frame, text=f"Всего страниц:{self.max_page}")
        self.max_page_label.pack(side=tk.RIGHT, padx=5, pady=5)


    def file_operations(self):
        def save_data():
            filename = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
            if filename:
                root = ET.Element("data")

                students_element = ET.SubElement(root, "students")
                for student in self.storage.students:
                    student_element = ET.SubElement(students_element, "student")
                    ET.SubElement(student_element, "group").text = str(student.group)
                    ET.SubElement(student_element, "name").text = str(student.name)
                    ET.SubElement(student_element, "course").text = str(student.course)
                    ET.SubElement(student_element, "total_works").text = str(student.total_works)
                    ET.SubElement(student_element, "completed_works").text = str(student.completed_works)
                    ET.SubElement(student_element, "language").text = str(student.programming_language)

                tree = ET.ElementTree(root)
                tree.write(filename, encoding='utf-8', xml_declaration=True)
                popup.destroy()

        def load_data():
            filename = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
            if filename:
                try:
                    tree = ET.parse(filename)
                    root = tree.getroot()

                    self.storage.students = []

                    for student_element in root.find("students"):
                        group = int(student_element.find("group").text)
                        name = student_element.find("name").text
                        course = int(student_element.find("course").text)
                        total_works = int(student_element.find("total_works").text)
                        completed_works = student_element.find("completed_works").text
                        programming_language = int(student_element.find("language").text)
                        self.storage.add_student(name, course, group, total_works, completed_works, programming_language)

                    self.update_students_list()
                    popup.destroy()

                except FileNotFoundError:
                    messagebox.showerror("Ошибка", "Файл не найден.")
                except ET.ParseError:
                    messagebox.showerror("Ошибка", "Неверный формат XML файла.")
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Ошибка при загрузке данных: {e}")

        popup = tk.Toplevel(self.master)
        popup.title("Файловые операции")

        save_button = tk.Button(popup, text="Сохранить", command=save_data)
        save_button.pack(pady=5)

        load_button = tk.Button(popup, text="Загрузить", command=load_data)
        load_button.pack(pady=5)

        close_button = tk.Button(popup, text="Закрыть", command=popup.destroy)
        close_button.pack(pady=5)



    def add_student(self):
        def save_student():
            name = name_entry.get()
            course = course_entry.get()
            group = group_entry.get()
            total_works = total_works_entry.get()
            completed_works = completed_works_entry.get()
            programming_language = programming_language_entry.get()
            if name and course and group and programming_language and completed_works and total_works:
                if not name.isalpha():
                    add_student_window.destroy()
                    messagebox.showwarning("Ошибка", "Имя студента должно быть строкой")
                    return
                if not course.isdigit():
                    add_student_window.destroy()
                    messagebox.showwarning("Ошибка", "Курс должен быть целым числом")
                    return
                if not group.isdigit():
                    add_student_window.destroy()
                    messagebox.showwarning("Ошибка", "Номер группы должен быть целым числом")
                    return
                if not total_works.isdigit():
                    add_student_window.destroy()
                    messagebox.showwarning("Ошибка", "Кол-во работ студента должно быть целым числом")
                    return
                if not completed_works.isdigit():
                    add_student_window.destroy()
                    messagebox.showwarning("Ошибка", "Кол-во вып. работ должен быть целым числом")
                    return
                if not programming_language.isalpha():
                    add_student_window.destroy()
                    messagebox.showwarning("Ошибка", "Язык прогр. должен быть строкой")
                    return
                self.controller.add_student(name, course, group, total_works, completed_works, programming_language)
                self.update_students_list()
            else:
                add_student_window.destroy()
                messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля")
                return

        add_student_window = tk.Toplevel(self.master)
        add_student_window.title("Добавить студента")

        name_label = tk.Label(add_student_window, text="Имя:")
        name_label.grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(add_student_window)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        group_label = tk.Label(add_student_window, text="Группа:")
        group_label.grid(row=1, column=0, padx=5, pady=5)
        group_entry = tk.Entry(add_student_window)
        group_entry.grid(row=1, column=1, padx=5, pady=5)

        course_label = tk.Label(add_student_window, text="Курс:")
        course_label.grid(row=2, column=0, padx=5, pady=5)
        course_entry = tk.Entry(add_student_window)
        course_entry.grid(row=2, column=1, padx=5, pady=5)

        total_works_label = tk.Label(add_student_window, text="Все работы:")
        total_works_label.grid(row=3, column=0, padx=5, pady=5)
        total_works_entry = tk.Entry(add_student_window)
        total_works_entry.grid(row=3, column=1, padx=5, pady=5)

        completed_works_label = tk.Label(add_student_window, text="Выполненные работы:")
        completed_works_label.grid(row=4, column=0, padx=5, pady=5)
        completed_works_entry = tk.Entry(add_student_window)
        completed_works_entry.grid(row=4, column=1, padx=5, pady=5)

        programming_language_label = tk.Label(add_student_window, text="Язык прогр.:")
        programming_language_label.grid(row=5, column=0, padx=5, pady=5)
        programming_language_entry = tk.Entry(add_student_window)
        programming_language_entry.grid(row=5, column=1, padx=5, pady=5)

        save_button = tk.Button(add_student_window, text="Сохранить", command=save_student)
        save_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)
            
    def update_students_list(self):
        self.student_list.delete(0, tk.END)

        students = self.controller.get_all_students()

        start_index = (self.current_page - 1) * self.max_students_per_page
        end_index = self.current_page * self.max_students_per_page

        for student in students[start_index:end_index]:
            self.student_list.insert(tk.END, student)

        self.page_label.config(text=f"Страница {self.current_page}")



    def search(self):
        search_option = simpledialog.askinteger("Поиск", "Выберите опцию:\n1. По имени студента\n2. По группе\n3. По курсу\n4. По языку прогр\n5. По числу работ\n6. По числу вып. работ\n7. По числу невып. работ")
        if search_option == 1:
            self.search_by_name()
        elif search_option == 2:
            self.search_by_group()
        elif search_option == 3:
            self.search_by_course()
        elif search_option == 4:
            self.search_by_programming_language()
        elif search_option == 5:
            self.search_by_total_works()
        elif search_option == 6:
            self.search_by_completed_works()
        elif search_option == 7:
            self.search_by_uncompleted_works()
        else:
            messagebox.showwarning("Ошибка", "Некорректный ввод")


    def search_by_name(self):
        def search_name():
            name = name_entry.get()
            if not name.isalpha():
                search_name_window.destroy()
                messagebox.showwarning("Ошибка", "Имя судента должен быть строкой")
                return

            found_students = self.controller.get_students_by_name(name)
            if found_students:
                results_window = tk.Toplevel(self.master)
                results_window.title(f"Найденные студенты {name}")

                results_list = tk.Listbox(results_window)
                results_list.pack(fill=tk.BOTH, expand=True)

                for student in found_students:
                    results_list.insert(tk.END, student)
            else:
                search_name_window.destroy()
                messagebox.showwarning("Ошибка", "Студенты не найдены")

        search_name_window = tk.Toplevel(self.master)
        search_name_window.title("Поиск по имени")

        name_label = tk.Label(search_name_window, text="Имя:")
        name_label.grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(search_name_window)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        search_button = tk.Button(search_name_window, text="Поиск", command=search_name)
        search_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    def search_by_group(self):
        def search_group_number():
            group = group_entry.get()
            if not group.isdigit():
                search_group_window.destroy()
                messagebox.showwarning("Ошибка", "Номер группы должен быть целым числом")
                return

            found_students = self.controller.get_students_by_group(group)
            if found_students:
                # Создаем новое окно для отображения найденных студентов
                results_window = tk.Toplevel(self.master)
                results_window.title(f"Найденные студенты в группе {group}")

                results_list = tk.Listbox(results_window)
                results_list.pack(fill=tk.BOTH, expand=True)

                for student in found_students:
                    results_list.insert(tk.END, student)
            else:
                search_group_window.destroy()
                messagebox.showwarning("Ошибка", "Студенты не найдены")

        search_group_window = tk.Toplevel(self.master)
        search_group_window.title("Поиск по группе")

        group_label = tk.Label(search_group_window, text="Номер группы:")
        group_label.grid(row=0, column=0, padx=5, pady=5)
        group_entry = tk.Entry(search_group_window)
        group_entry.grid(row=0, column=1, padx=5, pady=5)

        search_button = tk.Button(search_group_window, text="Поиск", command=search_group_number)
        search_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)


    def search_by_course(self):
        def search_course():
            course = course_entry.get()
            if not course.isdigit():
                search_course_window.destroy()
                messagebox.showwarning("Ошибка", "Курс должен быть целым числом")
                return

            found_students = self.controller.get_students_by_course(course)
            if found_students:
                results_window = tk.Toplevel(self.master)
                results_window.title(f"Найденные студенты на курсе {course}")

                results_list = tk.Listbox(results_window)
                results_list.pack(fill=tk.BOTH, expand=True)

                for student in found_students:
                    results_list.insert(tk.END, student)
            else:
                search_course_window.destroy()
                messagebox.showwarning("Ошибка", "Студенты не найдены")

        search_course_window = tk.Toplevel(self.master)
        search_course_window.title("Поиск по курсу")

        course_label = tk.Label(search_course_window, text="Номер курса:")
        course_label.grid(row=0, column=0, padx=5, pady=5)
        course_entry = tk.Entry(search_course_window)
        course_entry.grid(row=0, column=1, padx=5, pady=5)

        search_button = tk.Button(search_course_window, text="Поиск", command=search_course)
        search_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    def search_by_programming_language(self):
        def search_language():
            language = language_entry.get()
            if not language:
                search_language_window.destroy()
                messagebox.showwarning("Ошибка", "Введите язык программирования")
                return

            found_students = self.controller.get_students_by_programming_language(language)
            if found_students:
                results_window = tk.Toplevel(self.master)
                results_window.title(f"Найденные студенты, использующие язык {language}")

                results_list = tk.Listbox(results_window)
                results_list.pack(fill=tk.BOTH, expand=True)

                for student in found_students:
                    results_list.insert(tk.END, student)
            else:
                search_language_window.destroy()
                messagebox.showwarning("Ошибка", "Студенты не найдены")

        search_language_window = tk.Toplevel(self.master)
        search_language_window.title("Поиск по языку программирования")

        language_label = tk.Label(search_language_window, text="Язык:")
        language_label.grid(row=0, column=0, padx=5, pady=5)
        language_entry = tk.Entry(search_language_window)
        language_entry.grid(row=0, column=1, padx=5, pady=5)

        search_button = tk.Button(search_language_window, text="Поиск", command=search_language)
        search_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    def search_by_completed_works(self):
        def search_completed_works():
            completed_works = completed_works_entry.get()
            if not completed_works.isdigit():
                search_completed_works_window.destroy()
                messagebox.showwarning("Ошибка", "Количество выполненных работ должно быть целым числом")
                return

            found_students = self.controller.get_students_by_completed_works(completed_works)
            if found_students:
                results_window = tk.Toplevel(self.master)
                results_window.title(f"Найденные студенты с {completed_works} выполненными работами")

                results_list = tk.Listbox(results_window)
                results_list.pack(fill=tk.BOTH, expand=True)

                for student in found_students:
                    results_list.insert(tk.END, student)
            else:
                search_completed_works_window.destroy()
                messagebox.showwarning("Ошибка", "Студенты не найдены")

        search_completed_works_window = tk.Toplevel(self.master)
        search_completed_works_window.title("Поиск по числу выполненных работ")

        completed_works_label = tk.Label(search_completed_works_window, text="Число выполненных работ:")
        completed_works_label.grid(row=0, column=0, padx=5, pady=5)
        completed_works_entry = tk.Entry(search_completed_works_window)
        completed_works_entry.grid(row=0, column=1, padx=5, pady=5)

        search_button = tk.Button(search_completed_works_window, text="Поиск", command=search_completed_works)
        search_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    def search_by_total_works(self):
        def search_total_works():
            total_works = total_works_entry.get()
            if not total_works.isdigit():
                search_total_works_window.destroy()
                messagebox.showwarning("Ошибка", "Общее число работ должно быть целым числом")
                return

            found_students = self.controller.get_students_by_total_works(total_works)
            if found_students:
                results_window = tk.Toplevel(self.master)
                results_window.title(f"Найденные студенты с {total_works} работами")

                results_list = tk.Listbox(results_window)
                results_list.pack(fill=tk.BOTH, expand=True)

                for student in found_students:
                    results_list.insert(tk.END, student)
            else:
                search_total_works_window.destroy()
                messagebox.showwarning("Ошибка", "Студенты не найдены")

        search_total_works_window = tk.Toplevel(self.master)
        search_total_works_window.title("Поиск по общему числу работ")

        total_works_label = tk.Label(search_total_works_window, text="Общее число работ:")
        total_works_label.grid(row=0, column=0, padx=5, pady=5)
        total_works_entry = tk.Entry(search_total_works_window)
        total_works_entry.grid(row=0, column=1, padx=5, pady=5)

        search_button = tk.Button(search_total_works_window, text="Поиск", command=search_total_works)
        search_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    def search_by_uncompleted_works(self):
        def search_uncompleted_works():
            uncompleted_works = uncompleted_works_entry.get()
            if not uncompleted_works.isdigit():
                search_uncompleted_works_window.destroy()
                messagebox.showwarning("Ошибка", "Количество невыполненных работ должно быть целым числом")
                return

            found_students = self.controller.get_students_by_uncompleted_works(uncompleted_works)
            if found_students:
                results_window = tk.Toplevel(self.master)
                results_window.title(f"Найденные студенты с {uncompleted_works} невыполненными работами")

                results_list = tk.Listbox(results_window)
                results_list.pack(fill=tk.BOTH, expand=True)

                for student in found_students:
                    results_list.insert(tk.END, student)
            else:
                search_uncompleted_works_window.destroy()
                messagebox.showwarning("Ошибка", "Студенты не найдены")

        search_uncompleted_works_window = tk.Toplevel(self.master)
        search_uncompleted_works_window.title("Поиск по числу невыполненных работ")

        uncompleted_works_label = tk.Label(search_uncompleted_works_window, text="Число невып. работ:")
        uncompleted_works_label.grid(row=0, column=0, padx=5, pady=5)
        uncompleted_works_entry = tk.Entry(search_uncompleted_works_window)
        uncompleted_works_entry.grid(row=0, column=1, padx=5, pady=5)

        search_button = tk.Button(search_uncompleted_works_window, text="Поиск", command=search_uncompleted_works)
        search_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)





    def delete(self):
        search_option = simpledialog.askinteger("Удаление", "Выберите опцию:\n1. По имени студента\n2. По группе\n3. По курсу\n4. По языку прогр\n5. По числу работ\n6. По числу вып. работ\n7. По числу невып. работ")
        if search_option == 1:
            self.delete_by_name()
        elif search_option == 2:
            self.delete_by_group()
        elif search_option == 3:
            self.delete_by_course()
        elif search_option == 4:
            self.delete_by_programming_language()
        elif search_option == 5:
            self.delete_by_total_works()
        elif search_option == 6:
            self.delete_by_completed_works()
        elif search_option == 7:
            self.delete_by_uncompleted_works()
        else:
            messagebox.showwarning("Ошибка", "Некорректный ввод")


    def delete_by_group(self):
        def search_group():
            group_number = group_entry.get()
            if group_number:
                self.controller.delete_students_by_group(group_number)
                self.update_students_list()
                messagebox.showinfo("Удаление", f"Студенты из группы {group_number} удалены.")
                search_group_number_window.destroy()  # Закрываем окно поиска
            else:
                messagebox.showwarning("Ошибка", "Введите номер группы.")

        search_group_number_window = tk.Toplevel(self.master)
        search_group_number_window.title("Удаление по номеру группы")

        group_label = tk.Label(search_group_number_window, text="Номер группы:")
        group_label.grid(row=0, column=0, padx=5, pady=5)
        group_entry = tk.Entry(search_group_number_window)
        group_entry.grid(row=0, column=1, padx=5, pady=5)

        search_button = tk.Button(search_group_number_window, text="Удаление", command=search_group)
        search_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    def delete_by_name(self):
        def search_name():
            name = name_entry.get()
            if name:
                self.controller.delete_students_by_name(name)
                self.update_students_list()
                messagebox.showinfo("Удаление", f"Студент {name} удален.")
                search_name_window.destroy()
            else:
                messagebox.showwarning("Ошибка", "Введите имя студента.")

        search_name_window = tk.Toplevel(self.master)
        search_name_window.title("Удаление по имени")

        name_label = tk.Label(search_name_window, text="Имя студента:")
        name_label.grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(search_name_window)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        search_button = tk.Button(search_name_window, text="Удаление", command=search_name)
        search_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)


    def delete_by_course(self):
        def search_course():
            course_number = course_entry.get()
            if course_number:
                self.controller.delete_students_by_course(course_number)
                self.update_students_list()
                messagebox.showinfo("Удаление", f"Студенты с курса {course_number} удалены.")
                search_course_number_window.destroy()
            else:
                messagebox.showwarning("Ошибка", "Введите номер курса.")

        search_course_number_window = tk.Toplevel(self.master)
        search_course_number_window.title("Удаление по номеру курса")

        course_label = tk.Label(search_course_number_window, text="Номер курса:")
        course_label.grid(row=0, column=0, padx=5, pady=5)
        course_entry = tk.Entry(search_course_number_window)
        course_entry.grid(row=0, column=1, padx=5, pady=5)

        search_button = tk.Button(search_course_number_window, text="Удаление", command=search_course)
        search_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)


    def delete_by_programming_language(self):
        def search_language():
            language = language_entry.get()
            if language:
                self.controller.delete_students_by_programming_language(language)
                self.update_students_list()
                messagebox.showinfo("Удаление", f"Студенты, использующие язык {language}, удалены.")
                search_language_window.destroy()
            else:
                messagebox.showwarning("Ошибка", "Введите язык программирования.")

        search_language_window = tk.Toplevel(self.master)
        search_language_window.title("Удаление по языку программирования")

        language_label = tk.Label(search_language_window, text="Язык программирования:")
        language_label.grid(row=0, column=0, padx=5, pady=5)
        language_entry = tk.Entry(search_language_window)
        language_entry.grid(row=0, column=1, padx=5, pady=5)

        search_button = tk.Button(search_language_window, text="Удаление", command=search_language)
        search_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)


    def delete_by_total_works(self):
        def search_total_works():
            total_works = total_works_entry.get()
            if total_works:
                self.controller.delete_students_by_total_works(total_works)
                self.update_students_list()
                messagebox.showinfo("Удаление", f"Студенты с {total_works} работами удалены.")
                search_total_works_window.destroy()
            else:
                messagebox.showwarning("Ошибка", "Введите число работ.")

        search_total_works_window = tk.Toplevel(self.master)
        search_total_works_window.title("Удаление по числу работ")

        total_works_label = tk.Label(search_total_works_window, text="Число работ:")
        total_works_label.grid(row=0, column=0, padx=5, pady=5)
        total_works_entry = tk.Entry(search_total_works_window)
        total_works_entry.grid(row=0, column=1, padx=5, pady=5)

        search_button = tk.Button(search_total_works_window, text="Удаление", command=search_total_works)
        search_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)


    def delete_by_completed_works(self):
        def search_completed_works():
            completed_works = completed_works_entry.get()
            if completed_works:
                self.controller.delete_students_by_completed_works(completed_works)
                self.update_students_list()
                messagebox.showinfo("Удаление", f"Студенты с {completed_works} выполненными работами удалены.")
                search_completed_works_window.destroy()
            else:
                messagebox.showwarning("Ошибка", "Введите число выполненных работ.")

        search_completed_works_window = tk.Toplevel(self.master)
        search_completed_works_window.title("Удаление по числу выполненных работ")

        completed_works_label = tk.Label(search_completed_works_window, text="Число выполненных работ:")
        completed_works_label.grid(row=0, column=0, padx=5, pady=5)
        completed_works_entry = tk.Entry(search_completed_works_window)
        completed_works_entry.grid(row=0, column=1, padx=5, pady=5)

        search_button = tk.Button(search_completed_works_window, text="Удаление", command=search_completed_works)
        search_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    def delete_by_uncompleted_works(self):
        def search_uncompleted_works():
            uncompleted_works = uncompleted_works_entry.get()
            if uncompleted_works:
                self.controller.delete_students_by_uncompleted_works(uncompleted_works)
                self.update_students_list()
                messagebox.showinfo("Удаление", f"Студенты с {uncompleted_works} невыполненными работами удалены.")
                search_uncompleted_works_window.destroy()
            else:
                messagebox.showwarning("Ошибка", "Введите число невыполненных работ.")

        search_uncompleted_works_window = tk.Toplevel(self.master)
        search_uncompleted_works_window.title("Удаление по числу невыполненных работ")

        uncompleted_works_label = tk.Label(search_uncompleted_works_window, text="Число невыполненных работ:")
        uncompleted_works_label.grid(row=0, column=0, padx=5, pady=5)
        uncompleted_works_entry = tk.Entry(search_uncompleted_works_window)
        uncompleted_works_entry.grid(row=0, column=1, padx=5, pady=5)

        search_button = tk.Button(search_uncompleted_works_window, text="Удаление", command=search_uncompleted_works)
        search_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)


    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_students_list()

    def next_page(self):
        if self.current_page < self.max_page:
            self.current_page += 1
            self.update_students_list()

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
