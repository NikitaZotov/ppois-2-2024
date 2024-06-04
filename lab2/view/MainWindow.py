from view.DeleteWindow import DeleteWindow
from view.AddPlayerWindow import AddPlayerWindow
from view.AddTeamWindow import AddTeamWindow
from view.CreateFileWindow import CreateFileWindow
from view.SearchWindow import SearchWindow
from view.SearchResultWindow import FormSearchResultWindow
from view.CenteredWindowHelper import center_window

from controller.DataController import DataController

import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk
from tkinter import *
from tkinter import filedialog as fd

import re


class Application:
    def __init__(self):
        self.controller = None

        self.players_page = 0
        self.number_of_players_page = 10

        self.sports_page = 0
        self.number_of_sports_page = 10

        self.main_window = tk.Tk()

        self.main_window.minsize(width=1010, height=400)
        self.main_window.title('Football Teams Base')
        self.main_window.geometry('850x600')

        self.main_window.columnconfigure(index=0, weight=2)
        self.main_window.columnconfigure(index=1, weight=1)
        self.main_window.rowconfigure(index=1, weight=1)

        style = ttk.Style(self.main_window)
        style.theme_use('clam')
        style.configure('TCheckbutton', background='#4865A9', foreground='#001340')
        style.configure('TButton', background='#4865A9', foreground='#001340')

        center_window(self.main_window, 1000, 500)

        self.create_toolbar()
        self.configure_tabs()
        self.main_window.mainloop()

    def create_toolbar(self):

        # toolbar
        toolbar = ttk.Frame(self.main_window)
        toolbar.grid(row=0, column=0, columnspan=2, sticky=tk.EW, padx=2, pady=2)

        self.open_file_label = tk.StringVar()
        self.open_file_label.set("Opened file: None")

        toolbar_buttons = (
            ttk.Button(toolbar, text="Create file", command=self.create_file),
            ttk.Button(toolbar, text="Open file", command=self.open_file),
            ttk.Button(toolbar, text="Search", command=self.open_search_window),
            ttk.Button(toolbar, text="Delete", command=self.open_delete_window),
            ttk.Button(toolbar, text="Add team", command=self.open_add_sport_window),
            ttk.Button(toolbar, text="Add player", command=self.open_add_player_window)
        )
        for index, button in enumerate(toolbar_buttons):
            button.pack(padx=2, pady=0, side=tk.LEFT)
        label = tk.Label(toolbar, textvariable=self.open_file_label)
        label.pack(padx=2, pady=0, side=tk.LEFT)

    def check_sports_and_open_add_player_window(self):
        if not self.controller.get_sports():
            messagebox.showwarning("No teams", "There are no teams. Would you like to add one?")
        else:
            AddPlayerWindow(self.main_window, self)

    def _update_all_data(self, a=None, b=None, c=None):
        if self.controller is None:
            return
        self.update_sport_data()
        self.update_player_data()

    def close_data_source(self):
        self.controller = None

    def create_file(self):
        file_window = CreateFileWindow(self.main_window)  # create
        filename = file_window.show()
        if filename:
            self.open_file(filename)

    def open_add_player_window(self, event=None):
        if self.controller is None:
            tk.messagebox.showinfo(title='Error', message='Please, open data source')
        else:
            self.check_sports_and_open_add_player_window()

    def open_add_sport_window(self, event=None):
        if self.controller is None:
            tk.messagebox.showinfo(title='Error', message='Please, open data source')
        else:
            AddTeamWindow(self.main_window, self)

    def open_delete_window(self):
        if self.controller is None:
            tk.messagebox.showinfo(title='Error', message='Please, open data source')
        else:
            DeleteWindow(self.main_window, self)

    def open_search_window(self):
        if self.controller is None:
            tk.messagebox.showinfo(title='Error', message='Please, open data source')
        else:
            SearchWindow(self.main_window, self)

    def search_result(self, search) -> None:
        result_list = self.controller.search_players(search)

        if not result_list:
            messagebox.showinfo("Search", "Players were not found.")
            return
        else:
            messagebox.showinfo("Search", f"{len(result_list)} players were found.")

        FormSearchResultWindow(result_list)

    def open_file(self, filename_after_create: str = ""):

        if filename_after_create == "":
            filename = ""
            filetypes = [('XML files', '*.xml')]
            filename = fd.askopenfilename(title='Open file', filetypes=filetypes)

            if filename == "":
                return

            self.controller = DataController()
            self.open_file_label.set(f"Opened file: {filename}")
            self.controller.select_model(filename)

        else:

            self.controller = DataController()
            self.open_file_label.set(f"Opened file: {filename_after_create}")
            self.controller.select_model(filename_after_create)
            self.controller.creation()

        if self.controller is None:
            return

        self._update_all_data()
        self.table_sports_pages_combobox.state(["!disabled"])
        self.table_players_pages_combobox.state(["!disabled"])


    @staticmethod
    def is_valid_string(name):
        return all(re.match(r'^[А-ЯA-Z][а-яa-z]*$', word) for word in name.split())

    def configure_tabs(self):


        sports_panel = ttk.Labelframe(self.main_window, text="    Football team")
        sports_panel.grid(row=1, column=0, sticky=tk.NSEW)
        sports_panel.columnconfigure(index=0, weight=1)
        sports_panel.rowconfigure(index=0, weight=1)

        players_panel = ttk.Labelframe(self.main_window, text="    Players")
        players_panel.grid(row=1, column=1, sticky=tk.NSEW)
        players_panel.columnconfigure(index=0, weight=1)
        players_panel.rowconfigure(index=0, weight=1)
        # bottom toolbar

        def set_page_size_players(event):
            if self.controller is None:
                return
            try:
                if not self.table_players_pages_combobox.get():
                    return
                value = int(self.table_players_pages_combobox.get())
                if value < 1:
                    self.table_players_pages_combobox.set(page_count[1])
                    self.number_of_players_page = int(page_count[1])
                    self.players_page = 0
                    self.update_player_data()
                    messagebox.showerror("Error!", "Number should be > 0")
                else:
                    self.number_of_players_page = value
                    self.players_page = 0
                    self.update_player_data()
            except ValueError:
                self.table_players_pages_combobox.set(page_count[1])
                self.number_of_players_page = int(page_count[1])
                self.players_page = 0
                self.update_player_data()
                messagebox.showerror("Error!", "Incorrect number format")

        def set_page_size_sports(event):
            if self.controller is None:
                return
            try:
                if not self.table_sports_pages_combobox.get():
                    return
                value = int(self.table_sports_pages_combobox.get())
                if value < 1:
                    self.table_sports_pages_combobox.set(page_count[1])
                    self.number_of_sports_page = int(page_count[1])
                    self.sports_page = 0
                    self.update_sport_data()
                    messagebox.showerror("Error!", "Number should be > 0")
                else:
                    self.number_of_sports_page = value
                    self.sports_page = 0
                    self.update_sport_data()
            except ValueError:
                self.table_sports_pages_combobox.set(page_count[1])
                self.number_of_sports_page = int(page_count[1])
                self.sports_page = 0
                self.update_sport_data()
                messagebox.showerror("Error!", "Incorrect number format")
        # page size combobox
        page_count = ["5", "10", "20"]

        sport_tree_buttons = ttk.Frame(sports_panel)
        sport_tree_buttons.grid(row=1, column=0, sticky=tk.EW)

        sport_tree_next_page_btn = ttk.Button(master=sport_tree_buttons,
                                                  command=self.next_page_sports, text="Next page")
        sport_tree_next_page_btn.pack(padx=5, pady=2, side=tk.RIGHT)
        sport_tree_prev_page_btn = ttk.Button(master=sport_tree_buttons,
                                                  command=self.prev_page_sports, text="Prev page")
        sport_tree_prev_page_btn.pack(padx=3, pady=2, side=tk.RIGHT)

        self.table_sports_pages_combobox = ttk.Combobox(master=sport_tree_buttons, values=page_count, width=5)

        self.table_sports_pages_combobox.state(["disabled"])

        self.table_sports_pages_combobox.pack(side=tk.RIGHT)
        self.table_sports_pages_combobox.set(page_count[1])
        self.table_sports_pages_combobox.bind("<<ComboboxSelected>>", set_page_size_sports)
        self.table_sports_pages_combobox.bind("<KeyRelease>", set_page_size_sports)

        self.sport_page_label = ttk.Label(sport_tree_buttons, text="")
        self.sport_page_label.pack()
        self.update_page_label_sports()

        self.record_count_label_sports = ttk.Label(sport_tree_buttons, text="")
        self.record_count_label_sports.pack()
        self.update_record_count_label_sports()


        # Left side of main screen
        self.sport_tree = ttk.Treeview(master=sports_panel)
        self._configure_sports_table()

        self.sport_tree.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)

        # Right side of main screen
        self.player_tree = ttk.Treeview(master=players_panel)
        self._configure_players_table()

        self.player_tree.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)

        # bottom toolbar
        player_tree_buttons = ttk.Frame(players_panel)
        player_tree_buttons.grid(row=1, column=0, sticky=tk.EW)

        player_tree_next_page_btn = ttk.Button(master=player_tree_buttons,
                                                  command=self.next_page_players, text="Next page")
        player_tree_next_page_btn.pack(padx=3, pady=2, side=tk.RIGHT)
        player_tree_prev_page_btn = ttk.Button(master=player_tree_buttons,
                                                  command=self.prev_page_players, text="Prev page")
        player_tree_prev_page_btn.pack(padx=3, pady=2, side=tk.RIGHT)

        self.table_players_pages_combobox = ttk.Combobox(master=player_tree_buttons, values=page_count, width=5)
        self.table_players_pages_combobox.state(["disabled"])
        self.table_players_pages_combobox.pack(side=tk.RIGHT)
        self.table_players_pages_combobox.set(page_count[1])
        self.table_players_pages_combobox.bind("<<ComboboxSelected>>", set_page_size_players)
        self.table_players_pages_combobox.bind("<KeyRelease>", set_page_size_players)

        self.player_page_label = ttk.Label(player_tree_buttons, text="")
        self.player_page_label.pack()
        self.update_page_label_players()

        self.record_count_label_players = ttk.Label(player_tree_buttons, text="")
        self.record_count_label_players.pack()
        self.update_record_count_label_players()

    def _configure_sports_table(self):

        self.sports_page = 0
        sport_tree_columns = ("Name", "Player number", "Id")
        self.sport_tree.configure(columns=sport_tree_columns, show='headings')
        for id_title, title in enumerate(sport_tree_columns):
            self.sport_tree.heading(f"#{id_title + 1}", text=title)
            self.sport_tree.column(f"#{id_title + 1}", minwidth=len(title) + 15, width=len(title) + 10,
                                   stretch=True, anchor="center")
        self.load_sport_data()

    def _configure_players_table(self):

        self.players_page = 0
        player_tree_columns = ("Team", "Name", "Cast", "Position", "Hometown", "Birthday", "Id")
        self.player_tree.configure(columns=player_tree_columns, show='headings')
        for id_title, title in enumerate(player_tree_columns):
            self.player_tree.heading(f"#{id_title + 1}", text=title)
            self.player_tree.column(f"#{id_title + 1}", minwidth=len(title) + 10, width=len(title) + 82,
                                     stretch=True, anchor="center")
        self.load_player_data()

    def _configure_sports_table_size(self):
        sport_tree_columns = ("Name", "Player number", "Id")
        self.sport_tree.configure(columns=sport_tree_columns, show='headings')
#
        for id_title, title in enumerate(sport_tree_columns):
            self.sport_tree.heading(f"#{id_title + 1}", text=title)
            self.sport_tree.column(f"#{id_title + 1}", minwidth=len(title) + 117, width=len(title) + 100,
                                   stretch=True, anchor="center")

    def _configure_players_table_size(self):
        player_tree_columns = ("Team", "Name", "Cast", "Position", "Hometown", "Birthday", "Id")
        self.player_tree.configure(columns=player_tree_columns, show='headings')
        for id_title, title in enumerate(player_tree_columns):
            self.player_tree.heading(f"#{id_title + 1}", text=title)
            self.player_tree.column(f"#{id_title + 1}", minwidth=len(title) + 10, width=len(title) + 82,
                                     stretch=True, anchor="center")

    def load_player_data(self):
        try:
            self.player_tree.delete(*self.player_tree.get_children())
            query = """
                SELECT sport_id, name, cast, position, hometown, birthday, id
                FROM Players
                LIMIT ? OFFSET ?
                """
            parameters = (self.number_of_players_page, self.number_of_players_page * self.players_page)
            for record in self.controller.get_model().cursor.execute(query, parameters):
                self.player_tree.insert('', tk.END, values=record)
        except AttributeError:
            return

    def load_sport_data(self):
        try:
            self.sport_tree.delete(*self.sport_tree.get_children())
            query = """
                SELECT name, players_number, id
                FROM Teams
                LIMIT ? OFFSET ?
            """
            parameters = (self.number_of_sports_page, self.number_of_sports_page * self.sports_page)
            for record in self.controller.get_model().cursor.execute(query, parameters):
                self.sport_tree.insert('', tk.END, values=record)
        except AttributeError:
            return

    def update_player_data(self):
        for item in self.player_tree.get_children():
            self.player_tree.delete(item)
        start = self.players_page * self.number_of_players_page
        end = start + self.number_of_players_page
        for player in self.controller.get_players(start, end):
            self.player_tree.insert("", END, values=player.tuple())

        self.update_page_label_players()
        self.update_record_count_label_players()

    def update_sport_data(self):
        for item in self.sport_tree.get_children():
            self.sport_tree.delete(item)

        start = self.sports_page * self.number_of_sports_page
        end = start + self.number_of_sports_page
        for team in self.controller.get_sports(start, end):
            self.sport_tree.insert("", END, values=team.tuple())

        self.update_page_label_sports()
        self.update_record_count_label_sports()

    def update_record_count_label_players(self):
        try:
            total_records = self.controller.count_players_amount()
            start_index = self.players_page * self.number_of_players_page
            end_index = min((self.players_page + 1) * self.number_of_players_page, total_records)
            record_count_text = f"{end_index - start_index} of {total_records} entries"
            self.record_count_label_players.config(text=record_count_text)
        except AttributeError:
            self.record_count_label_players.config(text="No active data source")

    def update_record_count_label_sports(self):
        try:
            total_records = self.controller.count_sports_amount()
            start_index = self.sports_page * self.number_of_sports_page
            end_index = min((self.sports_page + 1) * self.number_of_sports_page, total_records)
            record_count_text = f"{end_index - start_index} of {total_records} entries"
            self.record_count_label_sports.config(text=record_count_text)
        except AttributeError:
            self.record_count_label_sports.config(text="No active data source")

    def next_page_players(self):
        if self.controller is None:
            return
        total_records = self.controller.count_players_amount()
        total_pages = (total_records + self.number_of_players_page - 1) // self.number_of_players_page
        if self.players_page < total_pages - 1:
            self.players_page += 1
        self.update_player_data()

    def next_page_sports(self):
        if self.controller is None:
            return
        total_records = self.controller.count_sports_amount()
        total_pages = (total_records + self.number_of_sports_page - 1) // self.number_of_sports_page

        if self.sports_page < total_pages - 1:
            self.sports_page += 1
        self.update_sport_data()

    def prev_page_players(self):
        if self.controller is None:
            return
        if self.players_page > 0:
            self.players_page -= 1
        self.update_player_data()

    def prev_page_sports(self):
        if self.controller is None:
            return
        if self.sports_page > 0:
            self.sports_page -= 1
        self.update_sport_data()

    def update_page_label_players(self):
        try:
            total_records = self.controller.count_players_amount()
            total_pages = (total_records + self.number_of_players_page - 1) // self.number_of_players_page
            self.player_page_label.config(text=f"Page {self.players_page + 1} of {total_pages}")
        except AttributeError:
            self.player_page_label.config(text="Page 1 of 1")

    def update_page_label_sports(self):
        try:
            total_records = self.controller.count_sports_amount()
            total_pages = (total_records + self.number_of_sports_page - 1) // self.number_of_sports_page
            self.sport_page_label.config(text=f"Page {self.sports_page + 1} of {total_pages}")
        except AttributeError:
            self.sport_page_label.config(text="Page 1 of 1")
