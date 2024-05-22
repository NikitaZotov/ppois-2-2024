import console
import tkinter as tk
from tkinter import messagebox
from person import Programmer
from programming_language import ProgrammingLanguage
from tkinter import ttk
from tkinter import scrolledtext

class View:
    def __init__(self,controller):
        self.root = tk.Tk()
        self.root.title("Compiler")
        self.root.geometry("1280x1024")
        self.root.resizable(False, False)
        self.controller = controller
        self.create_GUI()
        # self.controller = Controller()

    def run_programm(self):
        while True:
            try:
                choose = int(input("Выберите, что желаете использовать: 1 - CLI, 2 - GUI: "))
                if choose == 1:
                    print("Вы выбрали CLI")
                    console.start_program()
                elif choose == 2:
                    self.root.mainloop()
                else:
                    print("Некорректный выбор, попробуйте снова.")
                    continue
                break
            except ValueError:
                print("Значение не является целым числом. Пожалуйста, попробуйте снова.")

    def create_GUI(self):
        self.create_toolbar()

    def create_toolbar(self):
        toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)

        user_button = tk.Button(toolbar, text="Пользователь", command=self.create_user_window)
        user_button.pack(side=tk.LEFT, padx=2, pady=2)

        language_button = tk.Button(toolbar, text="Язык", command=self.create_language_window)
        language_button.pack(side=tk.LEFT, padx=2, pady=2)

        definition_button = tk.Button(toolbar, text="Описание", command=self.definition_window)
        definition_button.pack(side=tk.LEFT, padx=2, pady=2)

        safe_button = tk.Button(toolbar, text="Сохранить", command=self.safe_source_code)
        safe_button.pack(side=tk.LEFT, padx=2, pady=2)

        compiled_button = tk.Button(toolbar, text="Компиляция", command=self.compile)
        compiled_button.pack(side=tk.RIGHT, padx=2, pady=2)

        toolbar.pack(side=tk.TOP, fill=tk.X)
        self.part_to_write_source_code()
        self.canvas = tk.Canvas(self.root, width=1280, height=1024)
        self.canvas.pack()
        self.canvas.create_line(0, 0, 1280, 0, fill="black", width=10)

    def safe_source_code(self):
        self.controller.write_source_code(self.text_code)
        self.controller.model.safe_person_data()
        self.controller.write_source_code(self.text_code)

    def compile(self):
        source_code = self.text_code.get("1.0", tk.END)
        text = self.controller.check_prev_compilation(source_code)
        label_res = tk.Label(self.root, text=text, font=("Arial", 12),wraplength = 800,justify='left')
        label_res.place(x=5, y=710)
    def part_to_write_source_code(self):
        self.text_code = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=160, height=40)
        self.text_code.pack(padx=10, pady=10)
        if self.controller.load_person:
            self.controller.set_source_code(self.text_code)
    def definition_window(self):
        self.def_window = tk.Toplevel(self.root)
        self.def_window.title("Описание кода")
        self.def_window.geometry("320x250")
        label = tk.Label(self.def_window, text="Описание кода", font=("Arial", 14))
        label.pack(pady=5)
        text_area = scrolledtext.ScrolledText(self.def_window, wrap=tk.WORD, width=40, height=10)
        text_area.pack(padx=10, pady=10)
        text_area.insert("1.0", self.controller.get_definition())

        def clear_description():
            self.controller.model.programmer.source_code.description = ""
            text_area.delete("1.0", tk.END)
            text_area.insert("1.0", self.controller.get_definition())

        def apply_description():
            new_description = text_area.get("1.0",tk.END)
            self.controller.model.programmer.source_code.description = new_description
            text_area.delete("1.0", tk.END)
            text_area.insert("1.0", self.controller.get_definition())
            self.controller.safe_changes

        button_apply = tk.Button(self.def_window, text="Применить", command=apply_description)
        button_apply.place(x=215, y=215)
        button_clear = tk.Button(self.def_window, text="Очистить", command=clear_description)
        button_clear.place(x=10, y=215)

    def create_user_window(self):
        def check_source_values():
            self.controller.set_person_info(entry_fio,entry_years,entry_exp)
            self.controller.safe_changes()

        self.user_window = tk.Toplevel(self.root)
        self.user_window.title("Пользователь")
        self.user_window.geometry("320x250")
        self.create_user_labels()
        entry_fio = tk.Entry(self.user_window,width=50)
        entry_fio.place(x=5,y=80)
        entry_years = tk.Entry(self.user_window, width=50)
        entry_years.place(x=5, y=120)
        entry_exp = tk.Entry(self.user_window, width=50)
        entry_exp.place(x=5, y=160)
        self.controller.write_personal_info(entry_fio,entry_years,entry_exp)
        button_apply = tk.Button(self.user_window,text="Применить", command=check_source_values)
        button_apply.place(x=235,y=200)

    def write_to_entry_info(self,entry,text):
        entry.delete(0, "end")
        entry.insert(0,text)
    def create_user_labels(self):
        label = tk.Label(self.user_window, text="Данные пользователя", font=("Arial", 14))
        label.pack(pady=15)
        label_fio = tk.Label(self.user_window, text="Фамилия Имя Отчество:", font=("Arial", 12))
        label_fio.place(x=5, y=60)
        label_years = tk.Label(self.user_window, text="Полных лет:", font=("Arial", 12))
        label_years.place(x=5, y=100)
        label_exp = tk.Label(self.user_window, text="Опыт работы:", font=("Arial", 12))
        label_exp.place(x=5, y=140)
        text = "ФИО должно содержать от 2 до 3 слов\nПри указании возраста необходимо вводить целочисленное значение"
        label_inf = tk.Label(self.user_window, text=text, font=("Arial", 8), wraplength = 220,justify='left')
        label_inf.place(x=5, y=195)
    def create_language_window(self):
        self.lang_window = tk.Toplevel(self.root)
        self.lang_window.title("Настройки языка")
        self.lang_window.geometry("440x250")
        self.create_lang_labels()
        entry_name = tk.Entry(self.lang_window, width=35)
        entry_name.place(x=5, y=50)
        entry_ext = tk.Entry(self.lang_window, width=10)
        entry_ext.place(x=335, y=50)
        entry_key = tk.Entry(self.lang_window, width=35)
        entry_key.place(x=5, y=110)
        if self.controller.load_lang:
            text = self.controller.get_keywords()
        else:
            text = ""
        label_inf = tk.Label(self.lang_window, text=text, font=("Arial", 8), wraplength = 260,justify='left')
        label_inf.place(x=5, y=150)
        self.controller.load_language_settings(entry_name,entry_ext)
        combobox = ttk.Combobox(self.lang_window, values=["dataType", "singleOperator"], state="readonly")
        combobox.grid(row=0, column=0, padx=255, pady=110)
        combobox.current(0)

        def change_lang_settings():
            self.controller.check_language_settings(entry_name,entry_ext,entry_key,combobox,label_inf)
            self.controller.safe_changes()

        def clear_keywords():
            self.controller.clear_keywords(label_inf)
            self.controller.safe_changes()

        button_apply = tk.Button(self.lang_window, text="Применить", command=change_lang_settings)
        button_apply.place(x=320, y=200)

        button_clear = tk.Button(self.lang_window, text="Очистить", command=clear_keywords)
        button_clear.place(x=320, y=170)


    def create_lang_labels(self):

        label_name = tk.Label(self.lang_window, text="Название языка:", font=("Arial", 12))
        label_name.place(x=5, y=20)
        label_ext = tk.Label(self.lang_window, text="Расширение файла:", font=("Arial", 12))
        label_ext.place(x=255, y=20)
        label_key = tk.Label(self.lang_window, text="Ключевое слово:", font=("Arial", 12))
        label_key.place(x=5, y=90)
        label_type = tk.Label(self.lang_window, text="Тип:", font=("Arial", 12))
        label_type.place(x=255, y=90)
    def on_save(self):
        messagebox.showinfo("Инструмент", "Нажата кнопка Сохранить")

# Пример использования
if __name__ == "__main__":
    view = View()
    view.run_programm()
