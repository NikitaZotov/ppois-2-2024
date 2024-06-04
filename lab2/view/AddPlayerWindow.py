from __future__ import annotations
import re
from view.CenteredWindowHelper import center_window
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry


class AddPlayerWindow(tk.Toplevel):
    def __init__(self, master, application):
        super().__init__(master=master)
        self.title("Add player")
        self.application = application
        self.sport_list: list = self.application.controller.get_sports()
        self.cast_list: list = ["basic", "reserve", "n/a"]
        center_window(self, 233, 300)
        self.minsize(width=233, height=300)

        ttk.Label(self, text="Team name:").pack()
        self.player_sport_name_var = tk.StringVar()
        player_sport_name_combobox = ttk.Combobox(self, textvariable=self.player_sport_name_var,
                                                   values=[team.get_name() for team in self.sport_list],
                                                   state="readonly")
        player_sport_name_combobox.set(f'{self.sport_list[0].get_name()}')
        player_sport_name_combobox.pack()

        ttk.Label(self, text="Player name:").pack()
        self.player_name_entry = ttk.Entry(self)
        self.player_name_entry.pack()

        ttk.Label(self, text="Cast:").pack()
        self.player_cast_var = tk.StringVar()
        player_cast_combobox = ttk.Combobox(self, textvariable=self.player_cast_var,
                                                   values=[cast for cast in self.cast_list],
                                                   state="readonly")
        player_cast_combobox.set(f'{self.cast_list[0]}')
        player_cast_combobox.pack()

        ttk.Label(self, text="Position:").pack()
        self.player_position_entry = ttk.Entry(self)
        self.player_position_entry.pack()

        ttk.Label(self, text="Hometown:").pack()
        self.player_hometown_entry = ttk.Entry(self)
        self.player_hometown_entry.pack()

        ttk.Label(self, text="Birthday:").pack()
        self.player_birthdate_entry = DateEntry(self)
        self.player_birthdate_entry.pack()

        ttk.Button(self, text="Add", command=self.add_player_data).pack(pady=15)

    def add_player_data(self):

        sport_name = self.player_sport_name_var.get()
        name = self.player_name_entry.get().strip()  # Remove leading/trailing spaces
        cast = self.player_cast_var.get()
        position = self.player_position_entry.get().strip()  # Remove leading/trailing spaces
        hometown = self.player_hometown_entry.get()
        birthdate = self.player_birthdate_entry.get()

        # Check if any field is empty
        if not all((sport_name, name, cast, position, birthdate, hometown)):
            messagebox.showerror("Error!", "All fields shouldn't be empty.")
            self.player_name_entry.focus_set()
            return

        if not all(re.match("^[A-Za-z]+$", word) for word in name.split()):
            messagebox.showerror("Error!", "Incorrect name: expected symbols from [A-Z],[a-z].")
            self.player_name_entry.delete(0, 'end')
            self.player_name_entry.focus_set()
            return

        if self.application.controller.player_exists(sport_name, name, cast, position, hometown, birthdate):
            messagebox.showerror("Error", "Same player is already exist")
            self.player_name_entry.delete(0, 'end')
            self.player_sport_name_var.set("")
            self.player_cast_var.set("")
            self.player_position_entry.delete(0, 'end')
            self.player_birthdate_entry.delete(0, 'end')
            self.player_rank_var.set("")
            self.player_name_entry.focus_set()
            return

        self.application.controller.add_player(sport_name, name, cast, position, hometown, birthdate)
        messagebox.showinfo("Success!", "player has been successfully added.")
        self.application._update_all_data()
        self.destroy()

