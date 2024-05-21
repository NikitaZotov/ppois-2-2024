from view.DeleteWindow import DeleteWindow
from view.AddAthleteWindow import AddAthleteWindow
from view.AddSportWindow import AddSportWindow
from view.CreateFileWindow import CreateFileWindow
from view.SearchWindow import SearchWindow
from view.SearchResultWindow import FormSearchResultWindow
from view.CenteredWindowHelper import center_window

from presenter.DataPresenter import DataPresenter

import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk
from tkinter import *
from tkinter import filedialog as fd

import re


class Application:
    def __init__(self):
        self.presenter = None

        self.athletes_page = 0
        self.number_of_athletes_page = 10

        self.sports_page = 0
        self.number_of_sports_page = 10

        self.main_window = tk.Tk()

        self.main_window.minsize(width=1010, height=400)
        self.main_window.title('Sport Base')
        self.main_window.geometry('850x600')

        self.main_window.columnconfigure(index=0, weight=2)
        self.main_window.columnconfigure(index=1, weight=1)
        self.main_window.rowconfigure(index=1, weight=1)

        style = ttk.Style(self.main_window)
        style.configure('TCheckbutton', background='#90EE90')
        style.configure('TButton', background='#90EE90')

        self.__tree_view_enabled: BooleanVar = BooleanVar(value=False)
        self.__tree_view_enabled.trace('w', self._update_all_data)

        center_window(self.main_window, 1000, 500)

        self.create_toolbar()
        self.configure_tabs()
        self.main_window.mainloop()

    def create_toolbar(self):

        # toolbar
        toolbar = ttk.Frame(self.main_window)
        toolbar.grid(row=0, column=0, columnspan=2, sticky=tk.EW, padx=2, pady=2)

        toolbar_buttons = (
            ttk.Button(toolbar, text="Create file", command=self.create_file),
            ttk.Button(toolbar, text="Open file", command=self.open_file),
            ttk.Button(toolbar, text="Search", command=self.open_search_window),
            ttk.Button(toolbar, text="Delete", command=self.open_delete_window),
            ttk.Button(toolbar, text="Add sport", command=self.open_add_sport_window),
            ttk.Button(toolbar, text="Add athlete", command=self.open_add_athlete_window),
            ttk.Checkbutton(toolbar, text="Show Tree",
                            variable=self.__tree_view_enabled, command=self.tree_view_switch)
        )
        for index, button in enumerate(toolbar_buttons):
            button.pack(padx=2, pady=0, side=tk.LEFT)

    def check_sports_and_open_add_athlete_window(self):
        if not self.presenter.get_sports():
            messagebox.showwarning("No sports", "There are no sports. Would you like to add one?")
        else:
            AddAthleteWindow(self.main_window, self)

    def _update_all_data(self, a=None, b=None, c=None):
        if self.presenter is None:
            return
        self.update_sport_data()
        self.update_athlete_data()

    def close_data_source(self):
        self.presenter = None

    def create_file(self):
        file_window = CreateFileWindow(self.main_window)  # create
        filename = file_window.show()
        if filename:
            self.open_file(filename)

    def open_add_athlete_window(self, event=None):
        if self.presenter is None:
            tk.messagebox.showinfo(title='Error', message='Please, open data source')
        else:
            self.check_sports_and_open_add_athlete_window()

    def open_add_sport_window(self, event=None):
        if self.presenter is None:
            tk.messagebox.showinfo(title='Error', message='Please, open data source')
        else:
            AddSportWindow(self.main_window, self)

    def open_delete_window(self):
        if self.presenter is None:
            tk.messagebox.showinfo(title='Error', message='Please, open data source')
        else:
            DeleteWindow(self.main_window, self)

    def open_search_window(self):
        if self.presenter is None:
            tk.messagebox.showinfo(title='Error', message='Please, open data source')
        else:
            SearchWindow(self.main_window, self)

    def search_result(self, search) -> None:
        result_list = self.presenter.search_athletes(search)

        if not result_list:
            messagebox.showinfo("Search", "Athletes were not found.")
            return
        else:
            messagebox.showinfo("Search", f"{len(result_list)} athletes were found.")

        FormSearchResultWindow(result_list)

    def get_tree_view_value(self):
        return self.__tree_view_enabled.get()

    def tree_view_switch(self):

        if self.__tree_view_enabled.get():

            self._configure_sports_tree()
            self._configure_athletes_tree()
            self.athlete_tree['show'] = 'tree'
            self.sport_tree['show'] = 'tree'
        else:
            self._configure_sports_table_size()
            self._configure_athletes_table_size()
            self.athlete_tree['show'] = 'headings'
            self.sport_tree['show'] = 'headings'

        if self.presenter is None:
            return
        self._update_all_data()

    def open_file(self, filename_after_create: str = ""):

        if filename_after_create == "":
            filename = ""
            filetypes = [('DB files', '*.db'), ('XML files', '*.xml')]
            filename = fd.askopenfilename(title='Open file', filetypes=filetypes)

            if filename == "":
                return

            self.presenter = DataPresenter()
            self.presenter.select_model(filename)

        else:

            self.presenter = DataPresenter()
            self.presenter.select_model(filename_after_create)
            self.presenter.creation()

        if self.presenter is None:
            return

        self._update_all_data()
        self.table_sports_pages_combobox.state(["!disabled"])
        self.table_athletes_pages_combobox.state(["!disabled"])


    @staticmethod
    def is_valid_string(name):
        return all(re.match(r'^[А-ЯA-Z][а-яa-z]*$', word) for word in name.split())

    def configure_tabs(self):
        sports_panel = ttk.Labelframe(self.main_window, text="Sports")
        sports_panel.grid(row=1, column=0, sticky=tk.NSEW)
        sports_panel.columnconfigure(index=0, weight=1)
        sports_panel.rowconfigure(index=0, weight=1)

        athletes_panel = ttk.Labelframe(self.main_window, text="Athletes")
        athletes_panel.grid(row=1, column=1, sticky=tk.NSEW)
        athletes_panel.columnconfigure(index=0, weight=1)
        athletes_panel.rowconfigure(index=0, weight=1)
        # bottom toolbar
        def set_page_size_athletes(event):
            if self.presenter is None:
                return
            try:
                if not self.table_athletes_pages_combobox.get():
                    return
                value = int(self.table_athletes_pages_combobox.get())
                if value < 1:
                    self.table_athletes_pages_combobox.set(page_count[1])
                    self.number_of_athletes_page = int(page_count[1])
                    self.athletes_page = 0
                    self.update_athlete_data()
                    messagebox.showerror("Error!", "Number should be > 0")
                else:
                    self.number_of_athletes_page = value
                    self.athletes_page = 0
                    self.update_athlete_data()
            except ValueError:
                self.table_athletes_pages_combobox.set(page_count[1])
                self.number_of_athletes_page = int(page_count[1])
                self.athletes_page = 0
                self.update_athlete_data()
                messagebox.showerror("Error!", "Incorrect number format")

        def set_page_size_sports(event):
            if self.presenter is None:
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
        self.athlete_tree = ttk.Treeview(master=athletes_panel)
        self._configure_athletes_table()

        self.athlete_tree.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)

        # bottom toolbar
        athlete_tree_buttons = ttk.Frame(athletes_panel)
        athlete_tree_buttons.grid(row=1, column=0, sticky=tk.EW)

        athlete_tree_next_page_btn = ttk.Button(master=athlete_tree_buttons,
                                                  command=self.next_page_athletes, text="Next page")
        athlete_tree_next_page_btn.pack(padx=3, pady=2, side=tk.RIGHT)
        athlete_tree_prev_page_btn = ttk.Button(master=athlete_tree_buttons,
                                                  command=self.prev_page_athletes, text="Prev page")
        athlete_tree_prev_page_btn.pack(padx=3, pady=2, side=tk.RIGHT)

        self.table_athletes_pages_combobox = ttk.Combobox(master=athlete_tree_buttons, values=page_count, width=5)
        self.table_athletes_pages_combobox.state(["disabled"])
        self.table_athletes_pages_combobox.pack(side=tk.RIGHT)
        self.table_athletes_pages_combobox.set(page_count[1])
        self.table_athletes_pages_combobox.bind("<<ComboboxSelected>>", set_page_size_athletes)
        self.table_athletes_pages_combobox.bind("<KeyRelease>", set_page_size_athletes)

        self.athlete_page_label = ttk.Label(athlete_tree_buttons, text="")
        self.athlete_page_label.pack()
        self.update_page_label_athletes()

        self.record_count_label_athletes = ttk.Label(athlete_tree_buttons, text="")
        self.record_count_label_athletes.pack()
        self.update_record_count_label_athletes()

    def _configure_sports_table(self):

        self.sports_page = 0
        sport_tree_columns = ("Name", "Athletes number", "Id")
        self.sport_tree.configure(columns=sport_tree_columns, show='headings')
        for id_title, title in enumerate(sport_tree_columns):
            self.sport_tree.heading(f"#{id_title + 1}", text=title)
            self.sport_tree.column(f"#{id_title + 1}", minwidth=len(title) + 15, width=len(title) + 10,
                                   stretch=True, anchor="center")
        self.load_sport_data()

    def _configure_athletes_table(self):

        self.athletes_page = 0
        athlete_tree_columns = ("Sport", "Name", "Cast", "Position", "Title", "Rank", "Id")
        self.athlete_tree.configure(columns=athlete_tree_columns, show='headings')
        for id_title, title in enumerate(athlete_tree_columns):
            self.athlete_tree.heading(f"#{id_title + 1}", text=title)
            self.athlete_tree.column(f"#{id_title + 1}", minwidth=len(title) + 10, width=len(title) + 82,
                                     stretch=True, anchor="center")
        self.load_athlete_data()

    def _configure_sports_tree(self):
        self.sport_tree.configure(show='tree', columns=['Key', 'Value'])
        self.sport_tree.column("#0", minwidth=150, width=150, stretch=True, anchor="w")
        self.sport_tree.column("#1", minwidth=300, width=300, stretch=True, anchor="w")

    def _configure_athletes_tree(self):
        self.athlete_tree.configure(show='tree', columns=['Key', 'Value'])
        self.athlete_tree.column("#0", minwidth=170, width=170, stretch=True, anchor="w")
        self.athlete_tree.column("#1", minwidth=200, width=250, stretch=True, anchor="w")

    def _configure_sports_table_size(self):
        sport_tree_columns = ("Name", "Athletes number", "Id")
        self.sport_tree.configure(columns=sport_tree_columns, show='headings')

        for id_title, title in enumerate(sport_tree_columns):
            self.sport_tree.heading(f"#{id_title + 1}", text=title)
            self.sport_tree.column(f"#{id_title + 1}", minwidth=len(title) + 117, width=len(title) + 100,
                                   stretch=True, anchor="center")

    def _configure_athletes_table_size(self):
        athlete_tree_columns = ("Sport", "Name", "Cast", "Position", "Title", "Rank", "Id")
        self.athlete_tree.configure(columns=athlete_tree_columns, show='headings')
        for id_title, title in enumerate(athlete_tree_columns):
            self.athlete_tree.heading(f"#{id_title + 1}", text=title)
            self.athlete_tree.column(f"#{id_title + 1}", minwidth=len(title) + 10, width=len(title) + 82,
                                     stretch=True, anchor="center")

    def load_athlete_data(self):
        try:
            self.athlete_tree.delete(*self.athlete_tree.get_children())
            query = """
                SELECT sport_id, name, cast, position, title, rank, id
                FROM Athletes
                LIMIT ? OFFSET ?
                """
            parameters = (self.number_of_athletes_page, self.number_of_athletes_page * self.athletes_page)
            for record in self.presenter.get_model().cursor.execute(query, parameters):
                self.athlete_tree.insert('', tk.END, values=record)
        except AttributeError:
            return

    def load_sport_data(self):
        try:
            self.sport_tree.delete(*self.sport_tree.get_children())
            query = """
                SELECT name, athletes_number, id
                FROM Sports
                LIMIT ? OFFSET ?
            """
            parameters = (self.number_of_sports_page, self.number_of_sports_page * self.sports_page)
            for record in self.presenter.get_model().cursor.execute(query, parameters):
                self.sport_tree.insert('', tk.END, values=record)
        except AttributeError:
            return

    def update_athlete_data(self):
        for item in self.athlete_tree.get_children():
            self.athlete_tree.delete(item)
        start = self.athletes_page * self.number_of_athletes_page
        end = start + self.number_of_athletes_page
        for athlete in self.presenter.get_athletes(start, end):
            if not self.__tree_view_enabled.get():
                self.athlete_tree.insert("", END, values=athlete.tuple())
            else:
                athlete_row = self.athlete_tree.insert("", tk.END, text='athlete')
                sports = self.athlete_tree.insert(athlete_row, tk.END, text='Sport',
                                                       values=athlete.get_sport_name())
                self.athlete_tree.insert(athlete_row, tk.END, text='Name', values=athlete.get_name())
                self.athlete_tree.insert(athlete_row, tk.END, text='Cast', values=athlete.get_cast())
                self.athlete_tree.insert(athlete_row, tk.END, text='Position', values=athlete.get_position())
                self.athlete_tree.insert(athlete_row, tk.END, text='Title', values=athlete.get_title())
                self.athlete_tree.insert(athlete_row, tk.END, text='Id', values=athlete.get_id())
                sport = self.presenter.get_sport_by_name(athlete.get_sport_name())

                self.athlete_tree.insert(sports, tk.END, text='Athletes number',
                                         values=sport.get_athletes_number())
                self.athlete_tree.insert(sports, tk.END, text='Id', values=sport.get_id())

        self.update_page_label_athletes()
        self.update_record_count_label_athletes()

    def update_sport_data(self):
        for item in self.sport_tree.get_children():
            self.sport_tree.delete(item)

        start = self.sports_page * self.number_of_sports_page
        end = start + self.number_of_sports_page
        for sport in self.presenter.get_sports(start, end):
            if not self.__tree_view_enabled.get():
                self.sport_tree.insert("", END, values=sport.tuple())
            else:
                sport_row = self.sport_tree.insert("", tk.END, text='sport')
                self.sport_tree.insert(sport_row, tk.END, text='Name', values=sport.get_name())
                self.sport_tree.insert(sport_row, tk.END, text='Athletes number', values=sport.get_athletes_number())
                self.sport_tree.insert(sport_row, tk.END, text='Id', values=sport.get_id())

        self.update_page_label_sports()
        self.update_record_count_label_sports()

    def update_record_count_label_athletes(self):
        try:
            total_records = self.presenter.count_athletes_amount()
            start_index = self.athletes_page * self.number_of_athletes_page
            end_index = min((self.athletes_page + 1) * self.number_of_athletes_page, total_records)
            record_count_text = f"{end_index - start_index} of {total_records} entries"
            self.record_count_label_athletes.config(text=record_count_text)
        except AttributeError:
            self.record_count_label_athletes.config(text="No active data source")

    def update_record_count_label_sports(self):
        try:
            total_records = self.presenter.count_sports_amount()
            start_index = self.sports_page * self.number_of_sports_page
            end_index = min((self.sports_page + 1) * self.number_of_sports_page, total_records)
            record_count_text = f"{end_index - start_index} of {total_records} entries"
            self.record_count_label_sports.config(text=record_count_text)
        except AttributeError:
            self.record_count_label_sports.config(text="No active data source")

    def next_page_athletes(self):
        if self.presenter is None:
            return
        total_records = self.presenter.count_athletes_amount()
        total_pages = (total_records + self.number_of_athletes_page - 1) // self.number_of_athletes_page
        if self.athletes_page < total_pages - 1:
            self.athletes_page += 1
        self.update_athlete_data()

    def next_page_sports(self):
        if self.presenter is None:
            return
        total_records = self.presenter.count_sports_amount()
        total_pages = (total_records + self.number_of_sports_page - 1) // self.number_of_sports_page

        if self.sports_page < total_pages - 1:
            self.sports_page += 1
        self.update_sport_data()

    def prev_page_athletes(self):
        if self.presenter is None:
            return
        if self.athletes_page > 0:
            self.athletes_page -= 1
        self.update_athlete_data()

    def prev_page_sports(self):
        if self.presenter is None:
            return
        if self.sports_page > 0:
            self.sports_page -= 1
        self.update_sport_data()

    def update_page_label_athletes(self):
        try:
            total_records = self.presenter.count_athletes_amount()
            total_pages = (total_records + self.number_of_athletes_page - 1) // self.number_of_athletes_page
            self.athlete_page_label.config(text=f"Page {self.athletes_page + 1} of {total_pages}")
        except AttributeError:
            self.athlete_page_label.config(text="Page 1 of 1")

    def update_page_label_sports(self):
        try:
            total_records = self.presenter.count_sports_amount()
            total_pages = (total_records + self.number_of_sports_page - 1) // self.number_of_sports_page
            self.sport_page_label.config(text=f"Page {self.sports_page + 1} of {total_pages}")
        except AttributeError:
            self.sport_page_label.config(text="Page 1 of 1")
