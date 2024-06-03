from view.CenteredWindowHelper import center_window

from model.athlete import Athlete

from tkinter import *
from tkinter import ttk
import tkinter as tk


class FormSearchResultWindow(Toplevel):
    def __init__(self, athlete_list: list[Athlete]):
        super().__init__()
        self.athlete_list: list[Athlete] = athlete_list

        self.title('Search Result')
        center_window(self, 900, 250)
        self.minsize(width=900, height=250)
        self.geometry('900x250')
        self.columnconfigure(index=0, weight=1)
        self.rowconfigure(index=0, weight=1)

        self.athlete_tree = ttk.Treeview(master=self)  #
        athlete_tree_columns = ("Sport", "Name", "Cast", "Position", "Title", "Rank", "Id")  #
        self.athlete_tree.configure(columns=athlete_tree_columns, show='headings')  #
        for id_title, title in enumerate(athlete_tree_columns):  #
            self.athlete_tree.heading(f"#{id_title + 1}", text=title)  #
            self.athlete_tree.column(f"#{id_title + 1}", minwidth=len(title) + 10, width=len(title) + 82)  #
        self.athlete_tree.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)  #

        for athlete in self.athlete_list:
            values = (
                athlete.get_sport_name(),
                athlete.get_name(),
                athlete.get_cast(),
                athlete.get_position(),
                str(athlete.get_title()),
                athlete.get_rank(),
                str(athlete.get_id())
            )
            self.athlete_tree.insert('', 'end', values=values)
