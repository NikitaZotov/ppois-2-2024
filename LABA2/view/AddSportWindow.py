from view.CenteredWindowHelper import center_window

import re
import tkinter as tk
from tkinter import ttk, messagebox


class AddSportWindow(tk.Toplevel):
    def __init__(self, master, application):
        super().__init__(master=master)
        self.title("Add sport")
        self.application = application
        center_window(self, 228, 90)
        self.minsize(width=228, height=90)

        self.sport_list = ['Volleyball', 'Football', 'Basketball', 'Swimming']

        ttk.Label(self, text="Sport name:").pack()
        self.sport_name_var = tk.StringVar()
        self.sport_name_combobox = ttk.Combobox(self, textvariable=self.sport_name_var,
                                                   values=[sport for sport in self.sport_list])
        self.sport_name_combobox.set(f'{self.sport_list[0]}')
        self.sport_name_combobox.pack()
        ttk.Button(self, text="Add", command=self.add_sport_data).pack(pady=10)

    def add_sport_data(self):
        name = self.sport_name_var.get().strip()  # Remove leading/trailing spaces
        athletes_number = 0

        # Check if field are empty
        if not name:
            messagebox.showerror("Error!", "Field shouldn't be empty!")
            self.sport_name_combobox.focus_set()
            return

        # Check if name contains only letters
        if not all(re.match("^[A-Za-z]+$", word) for word in name.split()):
            messagebox.showerror("Error!", "Incorrect name: expected symbols from [A-Z],[a-z].")
            self.sport_name_var.set("")
            self.sport_name_combobox.focus_set()
            return

        if self.application.repo.sport_exists(name):
            messagebox.showerror("Error", "sport with this name is already exist")
            self.sport_name_var.set("")
            self.sport_name_combobox.focus_set()
            return

        self.application.repo.add_sport(name, athletes_number)
        messagebox.showinfo("Success!", "sport has been added.")
        self.application._update_all_data()
        self.destroy()
