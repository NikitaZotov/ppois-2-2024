from view.CenteredWindowHelper import center_window

from model.SearchModel import SearchModel
from model.CriteriaModel import Criteria
from tkcalendar import DateEntry
import tkinter as tk
from tkinter import ttk, messagebox
import re


class SearchWindow(tk.Toplevel):
    def __init__(self, master, application):
        super().__init__(master=master)
        self.title("Search player")
        center_window(self, 246, 470)
        self.minsize(width=246, height=470)
        self.application = application

        self.criteria_values = [
            Criteria.NAME.value,
            Criteria.SPORTNAME.value,
            Criteria.HOMETOWN.value,
            Criteria.BIRTHDATE.value,
            Criteria.POSITION.value,
            Criteria.CAST.value
        ]
        # Checkbox variables
        self.search_by_name = tk.BooleanVar()
        self.search_by_birthdate = tk.BooleanVar()
        self.search_by_position = tk.BooleanVar()
        self.search_by_cast = tk.BooleanVar()
        self.search_by_team = tk.BooleanVar()
        self.search_by_hometown = tk.BooleanVar()

        self.name_entry = None
        self.birthdate_entry = None
        self.sport_combobox = None
        self.hometown_entry = None
        self.cast_combobox = None
        self.position_entry = None

        self.cast_list: list = ["basic", "reserve", "n/a"]
        self.init_widgets()

    def init_widgets(self):
        def toggle_entry_state(entry_widget, checkbox_var):
            state = tk.NORMAL if checkbox_var.get() else tk.DISABLED
            entry_widget.config(state=state)

        def toggle_combobox_state(entry_widget, checkbox_var):
            state = "readonly" if checkbox_var.get() else tk.DISABLED
            entry_widget.config(state=state)

        # search by name
        name_frame = ttk.LabelFrame(self, text="Name")
        self.name_entry = ttk.Entry(name_frame, state=tk.DISABLED)
        self.name_entry.pack(side=tk.RIGHT)
        tk.Checkbutton(name_frame, variable=self.search_by_name,
                       command=lambda: toggle_entry_state(self.name_entry, self.search_by_name)
                       ).pack(side=tk.RIGHT)
        name_frame.pack(pady=10)
        # search by birthdate
        birthdate_frame = ttk.LabelFrame(self, text="Birthdate")
        self.birthdate_entry = DateEntry(birthdate_frame, state=tk.DISABLED)
        self.birthdate_entry.pack(side=tk.RIGHT)
        tk.Checkbutton(birthdate_frame, variable=self.search_by_birthdate,
                       command=lambda: toggle_entry_state(self.birthdate_entry, self.search_by_birthdate)
                       ).pack(side=tk.RIGHT)
        birthdate_frame.pack(pady=10)
        # search by team
        all_sports = self.application.controller.get_sports()
        sports_numbers = [team.get_name() for team in all_sports]
        sport_frame = ttk.LabelFrame(self, text="Team")
        self.sport_combobox = ttk.Combobox(sport_frame, values=sports_numbers, state=tk.DISABLED)
        self.sport_combobox.pack(side=tk.RIGHT)
        sport_frame.pack(pady=10)

        tk.Checkbutton(sport_frame, variable=self.search_by_team,
                       command=lambda: toggle_combobox_state(self.sport_combobox, self.search_by_team)
                       ).pack(side=tk.LEFT)

        # search by hometown
        hometown_frame = ttk.LabelFrame(self, text="Hometown")
        self.hometown_entry = ttk.Entry(hometown_frame, state=tk.DISABLED)
        self.hometown_entry.pack(side=tk.RIGHT)
        tk.Checkbutton(hometown_frame, variable=self.search_by_hometown,
                       command=lambda: toggle_entry_state(self.hometown_entry, self.search_by_hometown)
                       ).pack(side=tk.RIGHT)
        hometown_frame.pack(pady=10)

        # search by cast
        cast_frame = ttk.LabelFrame(self, text="Cast")
        self.cast_combobox = ttk.Combobox(cast_frame, values=self.cast_list, width=22, state=tk.DISABLED)
        self.cast_combobox.pack(side=tk.RIGHT)
        tk.Checkbutton(cast_frame, variable=self.search_by_cast,
                       command=lambda: toggle_combobox_state(self.cast_combobox, self.search_by_cast)
                       ).pack(side=tk.LEFT)
        cast_frame.pack(pady=10)

        # search by position
        position_frame = ttk.LabelFrame(self, text="Position")
        self.position_entry = ttk.Entry(position_frame, state=tk.DISABLED)
        self.position_entry.pack(side=tk.RIGHT)
        tk.Checkbutton(position_frame, variable=self.search_by_position,
                       command=lambda: toggle_entry_state(self.position_entry, self.search_by_position)
                       ).pack(side=tk.RIGHT)
        position_frame.pack(pady=10)

        ttk.Button(self, text="Search", command=self.search_player).pack(pady=10)

    def search_player(self):

        criteria_value = None

        if self.search_by_name.get():
            if self.name_entry.get() == "":
                messagebox.showerror("Error!", "Field name is empty")
                self.name_entry.focus_set()
                return
            if not all(re.match("^[A-Za-z]+$", word) for word in self.name_entry.get().strip().split()):
                messagebox.showerror("Error!", "Incorrect name: expected symbols from [A-Z],[a-z].")
                self.name_entry.delete(0, 'end')
                self.name_entry.focus_set()
                return
            criteria_value = Criteria.NAME.value
        if self.search_by_team.get():
            if self.sport_combobox.get() == "":
                messagebox.showerror("Error!", "Field team is empty")
                self.sport_combobox.focus_set()
                return
            criteria_value = Criteria.SPORTNAME.value
        if self.search_by_birthdate.get():
            if self.birthdate_entry.get() == "":
                messagebox.showerror("Error!", "Field birthdate is empty")
                self.birthdate_entry.focus_set()
                return
            criteria_value = Criteria.BIRTHDATE.value
        if self.search_by_hometown.get():
            if self.hometown_entry.get() == "":
                messagebox.showerror("Error!", "Field hometown is empty")
                self.hometown_entry.focus_set()
                return
            criteria_value = Criteria.HOMETOWN.value
        if self.search_by_cast.get():
            if self.cast_combobox.get() == "":
                messagebox.showerror("Error!", "Field cast is empty")
                self.cast_combobox.focus_set()
                return
            criteria_value = Criteria.CAST.value
        if self.search_by_position.get():
            if self.position_entry.get() == "":
                messagebox.showerror("Error!", "Field position is empty")
                self.position_entry.focus_set()
                return
            criteria_value = Criteria.POSITION.value
        if criteria_value is None:
            messagebox.showerror("Error!", "All fields are empty.")
            self.name_entry.focus_set()
            return
        search = SearchModel(
            self.name_entry.get(), self.birthdate_entry.get(), self.sport_combobox.get(), None,
            None, self.cast_combobox.get(), 0, 0, criteria_value)

        self.application.search_result(search)

        self.name_entry.delete(0, 'end')
        self.birthdate_entry.delete(0, 'end')
        self.sport_combobox.delete(0, 'end')
        self.hometown_entry.delete(0, 'end')
        self.cast_combobox.delete(0, 'end')
        self.position_entry.delete(0, 'end')
        self.destroy()







