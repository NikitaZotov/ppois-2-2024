from view.CenteredWindowHelper import center_window

from model.player import Player

from tkinter import *
from tkinter import ttk
import tkinter as tk


class FormSearchResultWindow(Toplevel):
    def __init__(self, player_list: list[Player]):
        super().__init__()
        self.player_list: list[Player] = player_list

        self.title('Search Result')
        center_window(self, 900, 250)
        self.minsize(width=900, height=250)
        self.geometry('900x250')
        self.columnconfigure(index=0, weight=1)
        self.rowconfigure(index=0, weight=1)

        self.player_tree = ttk.Treeview(master=self)  #
        player_tree_columns = ("Team", "Name", "Cast", "Position", "Hometown", "Birthday", "Id")  #
        self.player_tree.configure(columns=player_tree_columns, show='headings')  #
        for id_title, title in enumerate(player_tree_columns):  #
            self.player_tree.heading(f"#{id_title + 1}", text=title)  #
            self.player_tree.column(f"#{id_title + 1}", minwidth=len(title) + 10, width=len(title) + 82)  #
        self.player_tree.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)  #

        for player in self.player_list:
            values = (
                player.get_sport_name(),
                player.get_name(),
                player.get_cast(),
                player.get_position(),
                player.get_hometown(),
                str(player.get_birthday()),
                str(player.get_id())
            )
            self.player_tree.insert('', 'end', values=values)
