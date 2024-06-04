from tkinter import *
from tkinter import ttk
from model.pet import Pet
from model.vet import Vet
from model.dom_parser import PetRecordsManager
from tkinter import messagebox


class AddWindow(Tk):
    def __init__(self, file_path):
        super().__init__()
        self.pet = Pet()
        self.vet = Vet()
        self.file_path = file_path
        try:
            self.manager = PetRecordsManager(self.file_path)
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Вы не открыли файл с данными")
            self.destroy()
            return
        self.focus_set()
        self.entries = []
        self.entries_values = {}
        self.create_window()
        self.create_entries()

    def create_window(self):
        self.title("Добавление строки")
        self.geometry("400x300")
        self.resizable(width=False, height=False)

    def create_entries(self):
        Label(self, text="Имя:").grid(row=0, column=0, sticky="w")
        Label(self, text="Дата рождения:").grid(row=1, column=0, sticky="w")
        Label(self, text="Дата последнего посещения:").grid(row=2, column=0, sticky="w")
        Label(self, text="Ветеринар:").grid(row=3, column=0, sticky="w")
        Label(self, text="Диагноз:").grid(row=4, column=0, sticky="w")
        self.name_entry = ttk.Entry(self, width=35)
        self.name_entry.grid(row=0, column=1, sticky="w", pady=5)
        self.birth_date_entry = ttk.Entry(self, width=35)
        self.birth_date_entry.grid(row=1, column=1, sticky="w", pady=5)
        self.last_visit_date_entry = ttk.Entry(self, width=35)
        self.last_visit_date_entry.grid(row=2, column=1, sticky="w", pady=5)
        self.vet_entry = ttk.Entry(self, width=35)
        self.vet_entry.grid(row=3, column=1, sticky="w", pady=5)
        self.diagnosis_entry = ttk.Entry(self, width=35)
        self.diagnosis_entry.grid(row=4, column=1, sticky="w", pady=5)
        self.submit_button = ttk.Button(self, text="Создать словарь", command=self.create_row)
        self.submit_button.grid(row=5, column=0, columnspan=2, pady=5)

    def create_row(self):
        try:
            self.pet.name = self.name_entry.get()
            self.pet.birth_date = self.birth_date_entry.get()
            self.pet.last_visit_date = self.last_visit_date_entry.get()
            self.vet.fio = self.vet_entry.get()
            self.pet.diagnosis = self.diagnosis_entry.get()
            self.manager.add_pet_record(self.pet.name, self.pet.birth_date,
                                        self.pet.last_visit_date, self.pet.diagnosis, self.vet.fio)
            messagebox.showinfo("Успешно", "Поле успешно добавлено")
            self.destroy()
        except TypeError as er:
            messagebox.showerror("Ошибка", str(er))
            self.focus_set()


if __name__ == "__main__":
    app = AddWindow("../tests.xml")
    app.mainloop()
