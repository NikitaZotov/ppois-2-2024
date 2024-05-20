from __future__ import annotations
import re
from view.CenteredWindowHelper import center_window
import tkinter as tk
from tkinter import ttk, messagebox


class AddAthleteWindow(tk.Toplevel):
    def __init__(self, master, application):
        super().__init__(master=master)
        self.title("Add athlete")
        self.application = application
        self.sport_list: list = self.application.repo.get_sports()
        self.cast_list: list = ["basic", "reserve", "n/a"]
        self.rank_list: list = ["first junior", "second junior", "third junior",
                                "candidate master of sports", "master of sports"]
        center_window(self, 233, 300)
        self.minsize(width=233, height=300)

        ttk.Label(self, text="Sport name:").pack()
        self.athlete_sport_name_var = tk.StringVar()
        athlete_sport_name_combobox = ttk.Combobox(self, textvariable=self.athlete_sport_name_var,
                                                   values=[sport.get_name() for sport in self.sport_list],
                                                   state="readonly")
        athlete_sport_name_combobox.set(f'{self.sport_list[0].get_name()}')
        athlete_sport_name_combobox.pack()

        ttk.Label(self, text="Athlete name:").pack()
        self.athlete_name_entry = ttk.Entry(self)
        self.athlete_name_entry.pack()

        ttk.Label(self, text="Cast:").pack()
        self.athlete_cast_var = tk.StringVar()
        athlete_cast_combobox = ttk.Combobox(self, textvariable=self.athlete_cast_var,
                                                   values=[cast for cast in self.cast_list],
                                                   state="readonly")
        athlete_cast_combobox.set(f'{self.cast_list[0]}')
        athlete_cast_combobox.pack()

        ttk.Label(self, text="Position:").pack()
        self.athlete_position_entry = ttk.Entry(self)
        self.athlete_position_entry.pack()

        ttk.Label(self, text="Title:").pack()
        self.athlete_title_entry = ttk.Entry(self)
        self.athlete_title_entry.pack()

        ttk.Label(self, text="Rank:").pack()
        self.athlete_rank_var = tk.StringVar()
        athlete_rank_combobox = ttk.Combobox(self, textvariable=self.athlete_rank_var,
                                                   values=[rank for rank in self.rank_list],
                                                   state="readonly", width=25)
        athlete_rank_combobox.set(f'{self.rank_list[0]}')
        athlete_rank_combobox.pack()

        ttk.Button(self, text="Add", command=self.add_athlete_data).pack(pady=15)

    def add_athlete_data(self):

        sport_name = self.athlete_sport_name_var.get()
        name = self.athlete_name_entry.get().strip()  # Remove leading/trailing spaces
        cast = self.athlete_cast_var.get()
        position = self.athlete_position_entry.get().strip()  # Remove leading/trailing spaces
        title = self.athlete_title_entry.get().strip()  # Remove leading/trailing spaces
        rank = self.athlete_rank_var.get()

        # Check if any field is empty
        if not all((name, cast, position, title, sport_name, rank)):
            messagebox.showerror("Error!", "All fields shouldn't be empty.")
            self.athlete_name_entry.focus_set()
            return

        if not title.isdigit() or int(title) < 0:
            messagebox.showerror("Error!", "Incorrect title: expected natural value")
            self.athlete_title_entry.delete(0, 'end')
            self.athlete_title_entry.focus_set()
            return

        if not all(re.match("^[A-Za-z]+$", word) for word in name.split()):
            messagebox.showerror("Error!", "Incorrect name: expected symbols from [A-Z],[a-z].")
            self.athlete_name_entry.delete(0, 'end')
            self.athlete_name_entry.focus_set()
            return

        if self.application.repo.athlete_exists(sport_name, name, cast, position, title, rank):
            messagebox.showerror("Error", "Same athlete is already exist")
            self.athlete_name_entry.delete(0, 'end')
            self.athlete_sport_name_var.set("")
            self.athlete_cast_var.set("")
            self.athlete_position_entry.delete(0, 'end')
            self.athlete_title_entry.delete(0, 'end')
            self.athlete_rank_var.set("")
            self.athlete_name_entry.focus_set()
            return

        self.application.repo.add_athlete(sport_name, name, cast, position, title, rank)
        messagebox.showinfo("Success!", "athlete has been successfully added.")
        self.application._update_all_data()
        self.destroy()

