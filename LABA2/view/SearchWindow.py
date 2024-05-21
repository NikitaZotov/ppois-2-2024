from view.CenteredWindowHelper import center_window

from model.SearchModel import SearchModel
from model.CriteriaModel import Criteria

import tkinter as tk
from tkinter import ttk, messagebox
import re


class SearchWindow(tk.Toplevel):
    def __init__(self, master, application):
        super().__init__(master=master)
        self.title("Search athlete")
        center_window(self, 246, 290)
        self.minsize(width=246, height=290)
        self.application = application

        self.criteria_values = [
            Criteria.NAME.value,
            Criteria.SPORTNAME.value,
            Criteria.TITLE.value,
            Criteria.RANK.value
        ]
        # Checkbox variables
        self.search_by_name = tk.BooleanVar()
        self.search_by_sport_name = tk.BooleanVar()
        self.search_by_title = tk.BooleanVar()
        self.search_by_rank = tk.BooleanVar()

        self.name_entry = None
        self.sport_combobox = None
        self.title_max_entry = None
        self.title_min_entry = None
        self.rank_combobox = None
        self.title_default_min = None
        self.title_default_max = None

        self.rank_list: list = ["first junior", "second junior", "third junior",
                                "candidate master of sports", "master of sports"]
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

        # search by sport
        all_sports = self.application.presenter.get_sports()
        sports_numbers = [sport.get_name() for sport in all_sports]

        sport_frame = ttk.LabelFrame(self, text="Sport")

        self.sport_combobox = ttk.Combobox(sport_frame, values=sports_numbers, state=tk.DISABLED)
        self.sport_combobox.pack(side=tk.RIGHT)
        sport_frame.pack(pady=10)

        tk.Checkbutton(sport_frame, variable=self.search_by_sport_name,
                       command=lambda: toggle_combobox_state(self.sport_combobox, self.search_by_sport_name)
                       ).pack(side=tk.LEFT)

        # search by title
        title_frame = ttk.LabelFrame(self, text="Title")
        self.title_default_min = tk.IntVar(value=0)
        self.title_default_max = tk.IntVar(value=10)
        self.title_max_entry = ttk.Entry(title_frame, width=3, textvariable=self.title_default_max, state=tk.DISABLED)
        self.title_max_entry.pack(side=tk.RIGHT, padx=2)
        self.title_min_entry = ttk.Entry(title_frame, width=3, textvariable=self.title_default_min, state=tk.DISABLED)
        self.title_min_entry.pack(side=tk.RIGHT, padx=2)
        tk.Checkbutton(title_frame, variable=self.search_by_title,
                       command=lambda: (
                           toggle_entry_state(self.title_min_entry, self.search_by_title),
                           toggle_entry_state(self.title_max_entry, self.search_by_title))
                       ).pack(side=tk.RIGHT)
        title_frame.pack(pady=1)

        # search by rank
        rank_frame = ttk.LabelFrame(self, text="Rank")
        self.rank_combobox = ttk.Combobox(rank_frame, values=self.rank_list, width=22, state=tk.DISABLED)
        self.rank_combobox.pack(side=tk.RIGHT)
        tk.Checkbutton(rank_frame, variable=self.search_by_rank,
                       command=lambda: toggle_combobox_state(self.rank_combobox, self.search_by_rank)
                       ).pack(side=tk.LEFT)
        rank_frame.pack(pady=8)

        ttk.Button(self, text="Search", command=self.search_athlete).pack(pady=10)

    def search_athlete(self):

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
        if self.search_by_sport_name.get():
            if self.sport_combobox.get() == "":
                messagebox.showerror("Error!", "Field sport is empty")
                self.sport_combobox.focus_set()
                return
            criteria_value = Criteria.SPORTNAME.value
        if self.search_by_title.get():
            if not self.title_min_entry.get().isdigit():
                messagebox.showerror("Error!", "Incorrect title min")
                self.title_min_entry.delete(0, 'end')
                self.title_min_entry.focus_set()
                return
            if not self.title_max_entry.get().isdigit():
                messagebox.showerror("Error!", "Incorrect title max")
                self.title_max_entry.delete(0, 'end')
                self.title_max_entry.focus_set()
                return
            if int(self.title_min_entry.get()) > int(self.title_max_entry.get()):
                messagebox.showerror("Error!", "min > max")
                self.title_min_entry.delete(0, 'end')
                self.title_max_entry.delete(0, 'end')
                self.title_min_entry.focus_set()
                return
            criteria_value = Criteria.TITLE.value

        if self.search_by_rank.get():
            if self.rank_combobox.get() == "":
                messagebox.showerror("Error!", "Field rank is empty")
                self.rank_combobox.focus_set()
                return
            criteria_value = Criteria.RANK.value
        if criteria_value is None:
            messagebox.showerror("Error!", "All fields are empty.")
            self.name_entry.focus_set()
            return

        if self.search_by_title.get():
            search = SearchModel(
                self.name_entry.get(), self.sport_combobox.get(), self.title_min_entry.get(),
                self.title_max_entry.get(), self.rank_combobox.get(), 0, 0, criteria_value
            )
        else:
            search = SearchModel(
                self.name_entry.get(), self.sport_combobox.get(), None,
                None, self.rank_combobox.get(), 0, 0, criteria_value
            )
        self.application.search_result(search)

        self.name_entry.delete(0, 'end')
        self.sport_combobox.delete(0, 'end')
        self.title_min_entry.delete(0, 'end')
        self.title_max_entry.delete(0, 'end')
        self.rank_combobox.delete(0, 'end')
        self.destroy()







