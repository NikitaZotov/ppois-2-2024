import tkinter
from model import Model
from view import View
from person import Programmer
import console
from compiler import Compiler
class Controller:
    def __init__(self):
        self.model = Model()
        self.view = None
        self.load_person = None
        self.load_lang = None
        self.operators = {"+": ["int", "float", "string"], "-": ["int", "float"], "=": ["int", "float", "string"],
                 "*": ["int", "float"], "/": ["int", "float"]}

    def load_info(self):
        if self.model.load_info_person():
            print("Данные пользователя были загружены из файла")
            self.load_person = True
        else:
            print("Данные пользователя не были загружены из файла")
            self.load_person = False
        if self.model.load_info_language():
            print("Данные языка были загружены из файла")
            self.load_lang = True
        else:
            print("Данные языка не были загружены из файла")
            self.load_lang = False

    def check_prev_compilation(self,source_code):
        text = f"Компиляция проекта\n"
        info = self.model.get_info_about_language()
        text += info[0]
        if text[1]:
            step_comp = self.compilation()
            text += step_comp
        return text
    def write_personal_info(self,fio,age,exp):
        if self.load_person:
            self.view.write_to_entry_info(fio,self.model.programmer.full_name)
            self.view.write_to_entry_info(age, self.model.programmer.age)
            self.view.write_to_entry_info(exp, self.model.programmer.experience)

    def set_person_info(self,fio,age,exp):
        new_name = self.model.programmer.check_full_name(fio.get())
        new_age = self.model.programmer.check_age(int(age.get()))
        self.view.write_to_entry_info(fio, new_name)
        self.view.write_to_entry_info(age, str(new_age))
        self.view.write_to_entry_info(exp, exp.get())
        if new_name == "ФИО должно содержать от 2 до 3 слов" or new_name == "ФИО должно использовать только буквы и дефисы":
            new_name = ""
            self.load_person = False
        if new_age == "Возраст введён неверно":
            new_age = ""
            self.load_person = False
        self.model.set_new_person_data(new_name,new_age,exp.get())
        if self.model.programmer.full_name != "":
            self.load_person = True



    def run_programm(self):
        while True:
            try:
                choose = int(input("Выберите, что желаете использовать: 1 - CLI, 2 - GUI: "))
                if choose == 1:
                    print("Вы выбрали CLI")
                    console.start_program()
                elif choose == 2:
                    self.load_info()
                    self.view = View(self)
                    self.view.root.mainloop()
                else:
                    print("Некорректный выбор, попробуйте снова.")
                    continue
                break
            except ValueError:
                print("Значение не является целым числом. Пожалуйста, попробуйте снова.")

    def safe_changes(self):
        if self.load_person:
            self.model.safe_person_data()
        if self.load_lang:
            self.model.safe_language_data()

    def get_keywords(self):
        keywords = self.model.programming_language.get_key_word_list()
        text = "Ключевые слова, имеющиеся уже в системе: "
        i = 0
        for key in keywords:
            i += 1
            text += key
            if len(keywords) != i:
                text += ", "
            else:
                text += "."
        return text

    def load_language_settings(self,name,ext):
        if self.load_lang:
            self.view.write_to_entry_info(name,self.model.programming_language.name)
            self.view.write_to_entry_info(ext, self.model.programming_language.file_extension)

    def check_language_settings(self,name,ext,key,type,label):
        if len(name.get().split()) > 1:
            self.view.write_to_entry_info(name, "Название языка должно состоять из 1 слова")
        else:
            self.model.add_lang_name(name.get())
            self.view.write_to_entry_info(name, name.get())
        if len(ext.get().split()) > 1 and len(ext.get()) < 1:
            self.view.write_to_entry_info(ext, "")
        else:
            self.view.write_to_entry_info(ext, ext.get())
            self.model.add_lang_ext(ext.get())
        if len(key.get().split()) > 1:
            self.view.write_to_entry_info(key, "Ключевое слово должно быть записано без пробелов")
        elif key.get() == "":
            pass
        else:
            self.model.programming_language.add_new_key_word(key.get(),str(type.get()))
            self.view.write_to_entry_info(key, "")
        if len(name.get().split()) == 1 and len(ext.get().split()) == 1:
            self.load_lang = True
        text = self.get_keywords()
        label.destroy()
        label = tkinter.Label(self.view.lang_window, text=text, font=("Arial", 8), wraplength=260, justify='left')
        label.place(x=5, y=150)

    def clear_keywords(self,label):
        self.model.programming_language.clear_reserved_words()
        text = self.get_keywords()
        label.destroy()
        label = tkinter.Label(self.view.lang_window, text=text, font=("Arial", 8), wraplength=260, justify='left')
        label.place(x=5, y=150)

    def get_definition(self):
        return str(self.model.programmer.source_code.description)

    def write_source_code(self,text_entry):
        text = text_entry.get("1.0",tkinter.END)
        self.model.programmer.source_code.set_source_code(text)
        text_entry.delete("1.0",tkinter.END)
        text = self.model.programmer.source_code.get_source_code()
        text_entry.insert("1.0",text)

    def compilation(self):
        compiler = Compiler()
        compiler.compile_the_project(self.model.programmer.get_source_code(), self.model.programming_language, self.operators)
        return compiler.get_result()

    def set_source_code(self,entry):
        entry.insert("1.0",self.model.programmer.source_code.get_source_code())