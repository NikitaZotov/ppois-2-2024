import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox
from tkcalendar import Calendar, DateEntry
from tkinter import *
from Model.tournament import Tournament
from Controller.main_controller import MainController
delete_list = ["Название турнира",
               "Дата проведения",
               "Название спорта",
               "Имя победителя",
               "Размер призового фонда",
               "Приз победителя", ]


class DeleteInterface(tk.Toplevel):
    def __init__(self, master, application, type_delete: int):
        super().__init__(master)
        self.master = master
        self.application = application
        self.controller = application.controller
        self.type_delete = type_delete
        # delete frame
        self.frame_delete = tk.Frame(self)
        self.delete_text = ""
        if self.type_delete == 0 or self.type_delete == 3:
            self.delete_text = delete_list[self.type_delete]
            self.delete_entry = ttk.Entry(self.frame_delete)
            self.delete_entry.grid(row=1, column=0)
        elif self.type_delete == 2:
            self.delete_text = delete_list[self.type_delete]
            self.delete_entry = ttk.Combobox(self.frame_delete, values=self.get_sports())
            self.delete_entry.grid(row=1, column=0)
        elif self.type_delete == 1:
            self.delete_text = delete_list[self.type_delete]
            self.delete_entry = DateEntry(self.frame_delete, date_pattern="YYYY-mm-dd")
            self.delete_entry.grid(row=1, column=0)
        elif 4 <= self.type_delete <= 5:
            check = (self.master.register(self.is_number), "%P")
            self.delete_text = delete_list[self.type_delete]
            self.delete_label_min = tk.Label(self.frame_delete, text="мин. значение")
            self.delete_entry_min = ttk.Entry(self.frame_delete, validate="key", validatecommand=check)
            self.delete_label_min.grid(row=1, column=0)
            self.delete_entry_min.grid(row=2, column=0)
            self.delete_label_max = tk.Label(self.frame_delete, text="макс. значение")
            self.delete_entry_max = ttk.Entry(self.frame_delete, validate="key", validatecommand=check)
            self.delete_label_max.grid(row=1, column=1)
            self.delete_entry_max.grid(row=2, column=1)
            print(delete_list[self.type_delete])
        self.delete_btn = tk.Button(self.frame_delete, text="Удалить", command=self.delete_button)
        print(self.type_delete)
        self.delete_label = tk.Label(self.frame_delete, text=self.delete_text)
        self.delete_label.grid(row=0, column=0)
        self.delete_btn.grid(row=3, column=0)
        self.frame_delete.grid(row=3, column=0)

    def delete_button(self):
        if 4 <= self.type_delete <= 5:
            try:
                delete_data_max = float(self.delete_entry_max.get())
                delete_data_min = float(self.delete_entry_min.get())
            except ValueError:
                return None
            result = self.controller.delete_data(self.type_delete, delete_data_min, second_elem=delete_data_max)
        else:
            if len(self.delete_entry.get()) == 0:
                return None
            delete_data = self.delete_entry.get()
            result = self.controller.delete_data(self.type_delete, delete_data)
        tkinter.messagebox.showinfo(message=f"Было удалено  {result}")
        self.application.update_list()

    def get_sports(self):
        return self.controller.get_sports()

    def is_number(self, number):

        try:
            float(number)
            return True
        except ValueError:
            if len(number) == 0:
                return True
            return False
