import tkinter as tk

from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showwarning
from ttkthemes import ThemedStyle

from controller.xmlparser import XMLParser
from controller.filter import Filter
from view.adddialog import AddDialog
from view.searchdialog import SearchDialog
from view.deletedialog import DeleteDialog


class App:

    def __init__(self):
        self.file = None
        self.main_window = tk.Tk()
        self.main_window.minsize(width=1000, height=800)
        self.main_window['bg'] = 'gray22'
        self.main_window.title("Tournaments")
        self.main_window.columnconfigure(index=0, weight=1)
        self.main_window.rowconfigure(index=1, weight=1)
        
        self.theme = ThemedStyle(master=self.main_window)
        self.theme.set_theme('black')

        self.tournaments_frame = ttk.Labelframe(self.main_window, text="Tournaments")
        self.tournaments_frame.grid(row=1, column=0, sticky=tk.NSEW)
        self.tournaments_frame.columnconfigure(index=0, weight=1)
        self.tournaments_frame.rowconfigure(index=0, weight=1)
        self.tournaments = ttk.Treeview(master=self.tournaments_frame)
        self.write_tournaments()
        self.tournaments.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)
        

        self.toolbar = ttk.Frame(self.main_window)
        self.toolbar.grid(row=0, column=0, columnspan=2, sticky=tk.EW, padx=2, pady=2)
        
        self.buttons = [ttk.Button(self.toolbar, text="Open XML", command=self.open),
                        ttk.Button(self.toolbar, text="Create XML", command=self.create),
                        ttk.Button(self.toolbar, text="Close XML", command=self.close),
                        ttk.Button(self.toolbar, text="Add tournament", command=self.add),
                        ttk.Button(self.toolbar, text="Find tournaments", command=self.find),
                        ttk.Button(self.toolbar, text="Delete tournaments", command=self.delete),
                        ttk.Button(self.toolbar, text="Reset filter", command=self.reset_filters)]
        
        for button in self.buttons: button.pack(padx=2, pady=0, side=tk.LEFT)

        self.curr_page = 1
        self.pages_amount = 1

        self.flipping = ttk.Frame(self.tournaments_frame)
        self.flipping.grid(row=1, column=0, sticky=tk.EW)
        self.next_button = ttk.Button(master=self.flipping, text=">", width=1)
        self.next_button.pack(padx=3, pady=0, side=tk.RIGHT)
        self.prev_button = ttk.Button(master=self.flipping, text="<", width=1)
        self.prev_button.pack(padx=3, pady=0, side=tk.RIGHT)
        self.last_page_button = ttk.Button(master=self.flipping, text="Last")
        self.last_page_button.pack(padx=3, pady=0, side=tk.RIGHT)
        self.first_page_button = ttk.Button(master=self.flipping, text="First")
        self.first_page_button.pack(padx=3, pady=0, side=tk.RIGHT)
        
        
        size = ['3', '5', '10', '20', '50']

        self.paging = ttk.Combobox(master=self.flipping, values=size, width=3)
        self.paging.pack(side=tk.RIGHT)
        self.paging.set(size[2])
        self.paging.bind('<<ComboboxSelected>>', self.set_size)
        self.pages_info = ttk.Label(master=self.flipping)
        self.pages_info.pack(side=tk.RIGHT, padx=5)

        self.search_filter = Filter()
        self.delete_filter = Filter()

    def update_data(self):
        if not self.file: return

        for tournament in self.tournaments.get_children():
            self.tournaments.delete(tournament)

        for tournament in self.file.filter_tournaments(self.search_filter):
            self.tournaments.insert(parent="", index=tk.END, values=[tournament.title, tournament.date, 
                                                          tournament.sport, tournament.winner.name,
                                                          tournament.winner.surname, 
                                                          tournament.winner.middlename,
                                                          tournament.prize, tournament.winner_prize])
        
        tournaments_amount = len(self.file.filter_tournaments(self.search_filter))
        self.pages_amount = int(tournaments_amount / self.search_filter.page_size)

        info = f"Curr. page {self.search_filter.page_number} of {self.pages_amount}"
        info += f"Total writings: {tournaments_amount}. Writings on the page: "
        self.pages_info.configure(text=info)
        self.pages_info.update()

    def write_tournaments(self):

        columns = ['Title', 'Date', 'Sport', "Winner's name", "Winner's surname", 
                   "Winner's middlename", 'Prize', "Winner's prize"]
        
        self.tournaments.configure(columns=columns, show='headings')

        for i, column in enumerate(columns):
            self.tournaments.heading(f"#{i + 1}", text=column)
            self.tournaments.column(f"#{i + 1}", width=len(column) + 20)

    def set_size(self, event):
        self.curr_page = 1
        self.search_filter.page_number = self.curr_page
        self.search_filter.page_size = int(self.paging.get())
        self.update_data()

    def next_page(self):
        if self.search_filter.page_number < self.pages_amount:
            self.search_filter.page_number += 1
            self.update_data()

    def prev_page(self):
        if self.search_filter.page_number != 1:
            self.search_filter.page_number -= 1
            self.update_data()

    def first_page(self):
        self.search_filter.page_number = 1
        self.update_data()

    def last_page(self):
        self.search_filter.page_number = self.pages_amount
        self.update_data()

    def create(self):
        
        self.close()

        file = filedialog.asksaveasfile(initialfile='Tournaments.xml', defaultextension='.xml',
                                        filetypes={('XML files', '*.xml')})

        if file:
            self.file = XMLParser(file.name)
            self.file.init_xml()
            self.update_data()

    def open(self):
        
        self.close()

        filepath = filedialog.askopenfilename(title='Open XML', filetypes={('XML files', '*.xml')})

        if filepath: 
            self.file = XMLParser(filepath)
            self.file.init_xml()
            self.update_data()

    def close(self):
        self.file = None
        self.reset_filters()
        self.update_data()
        
    def reset_filters(self):
        self.search_filter = Filter()
        self.delete_filter = Filter()

        self.update_data()

    def add(self): 
        if not self.file: showwarning(title="Warning", message='Open .xml file')
        else: AddDialog(master=self.main_window, app=self)

    def find(self): 
        if not self.file: showwarning(title="Warning", message='Open .xml file')
        else: SearchDialog(master=self.main_window, app=self)

    def delete(self): 
        if not self.file: showwarning(title="Warning", message='Open .xml file')
        else: DeleteDialog(master=self.main_window, app=self)













