from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from model.dom_parser import PetRecordsManager
import xml.sax
from model.sax_parsers.criteria import LastVisitVetNameHandler, DiagnosisPhraseHandler, NameBirthDateHandler
from model.pet import Pet
from model.vet import Vet


class DeleteWindow(Tk):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.pet_parser = xml.sax.make_parser()
        self.pet_handler = None
        self.pet = Pet()
        self.vet = Vet()
        try:
            self.manager = PetRecordsManager(main_window.file_path)
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Вы не открыли файл с данными")
            self.destroy()
            return
        self.var = IntVar(self)
        self.entries = {}
        self.labels = ['name', 'birth_date', 'last_visit', 'vet', 'diagnosis']
        self.create_window()
        self.create_entries()
        self.create_radiobuttons()

    def create_window(self):
        self.title("Поиск строк")
        self.geometry("400x450")
        self.resizable(width=False, height=False)

    def create_entries(self):
        for i, label_name in enumerate(self.labels):
            entry = ttk.Entry(self, name=label_name)
            self.entries[label_name] = entry

    def create_radiobuttons(self):
        label = Label(self, text="Выберите способ поиска для удаления:", name='main_label')
        label.grid(row=0, column=0, pady=10, sticky='w')
        rb_name_birth = ttk.Radiobutton(self, text="По имени и дате рождения",
                                        command=self.on_radio_button_clicked, variable=self.var, value=1)
        rb_name_birth.grid(row=1, column=0, pady=5, sticky="w")
        rb_visit_vet = ttk.Radiobutton(self, text="По последнему визиту и врачу",
                                       command=self.on_radio_button_clicked, variable=self.var, value=2)
        rb_visit_vet.grid(row=2, column=0, pady=5, sticky="w")
        rb_diagnosis = ttk.Radiobutton(self, text="По фразе из диагноза",
                                       command=self.on_radio_button_clicked, variable=self.var, value=3)
        rb_diagnosis.grid(row=3, column=0, pady=5, sticky="w")

    def on_radio_button_clicked(self):
        for widget in self.winfo_children():
            if widget.winfo_name() != "main_label" and isinstance(widget, (Label, ttk.Entry)):
                widget.grid_forget()
        choice = self.var.get()
        if choice == 1:
            self.name_birth_entry()
            self.create_button()
        elif choice == 2:
            self.visit_vet_entry()
            self.create_button()
        elif choice == 3:
            self.diagnosis_entry()
            self.create_button()

    def name_birth_entry(self):
        label_name = Label(self, text="Имя питомца")
        label_birth = Label(self, text="Дата рождения")
        label_name.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.entries['name'].grid(row=5, column=0, padx=10, pady=5)
        label_birth.grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.entries['birth_date'].grid(row=7, column=0, padx=10, pady=5)

    def visit_vet_entry(self):
        label_visit = Label(self, text="Дата последнего посещения")
        label_vet = Label(self, text="ФИО врача")
        label_visit.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.entries['last_visit'].grid(row=5, column=0, padx=10, pady=5)
        label_vet.grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.entries['vet'].grid(row=7, column=0, padx=10, pady=5)

    def diagnosis_entry(self):
        label_diagnosis = Label(self, text="Имя питомца")
        label_diagnosis.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.entries['diagnosis'].grid(row=5, column=0, padx=10, pady=5)

    def find_click(self):
        try:
            if self.var.get() == 1:
                self.entries['name'] = self.pet.name = self.entries['name'].get()
                self.entries['birth_date'] = self.pet.birth_date = self.entries['birth_date'].get()
                self.pet_handler = NameBirthDateHandler(self.pet.name, self.pet.birth_date)
                self.pet_parser.setContentHandler(self.pet_handler)
                self.pet_parser.parse(self.main_window.file_path)
                self.manager.remove_by_name_and_birth_date(self.pet.name, self.pet.birth_date)
            elif self.var.get() == 2:
                self.entries['last_visit'] = self.pet.last_visit_date = self.entries['last_visit'].get()
                self.entries['vet'] = self.vet.fio = self.entries['vet'].get()
                self.pet_handler = LastVisitVetNameHandler(self.pet.last_visit_date, self.vet.fio)
                self.pet_parser.setContentHandler(self.pet_handler)
                self.pet_parser.parse(self.main_window.file_path)
                self.manager.remove_by_last_visit_and_fio(self.pet.last_visit_date, self.vet.fio)
            elif self.var.get() == 3:
                self.entries['diagnosis'] = self.pet.diagnosis = self.entries['diagnosis'].get()
                self.pet_handler = DiagnosisPhraseHandler(self.pet.diagnosis)
                self.pet_parser.setContentHandler(self.pet_handler)
                self.pet_parser.parse(self.main_window.file_path)
                self.manager.remove_by_diagnosis_phrase("Вакцин")
            messagebox.showinfo("Успех", f'Было удалено {len(self.pet_handler.result)} записей')
        except TypeError:
            messagebox.showerror("Ошибка", str(TypeError))

    def create_button(self):
        button = ttk.Button(self, text='Удалить', command=self.find_click)
        button.grid(row=8, column=3)
