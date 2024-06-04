from datetime import datetime as dt

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror

from tkcalendar import Calendar
from ttkthemes import ThemedStyle

class DeleteDialog(tk.Toplevel):

    def __init__(self, master, app):
        super().__init__(master=master)
        self.app = app
        self.minsize(height=400, width=300)
        self['bg'] = 'gray22'
        self.theme = ThemedStyle(master=self)
        self.theme.set_theme('black')
        self.title("Delete tournaments")

        self.title_frame = ttk.Labelframe(self, text="Tournament title")
        self.input_title = ttk.Entry(master=self.title_frame, width=40)
        self.input_title.pack()
        self.title_frame.pack(pady=5)

        self.datepicker_frame = ttk.LabelFrame(self, text="Tournament date")
        self.datepicker = Calendar(master=self.datepicker_frame)
        self.datepicker._remove_selection()
        self.datepicker.pack()
        self.datepicker_frame.pack()

        self.sport_frame = ttk.Labelframe(self, text="Tournament sport")
        self.sports = tuple(self.app.file.get_sports())
        self.input_sport = ttk.Combobox(master=self.sport_frame, width=40, values=self.sports)
        self.input_sport.pack()
        self.sport_frame.pack(pady=5)

        self.winner_frame = ttk.Labelframe(self, text="Tournament winner")
        self.name_label = ttk.Label(master=self.winner_frame, text='Name')
        self.input_name = ttk.Entry(master=self.winner_frame, width=40)
        self.name_label.pack()
        self.input_name.pack()
        self.surname_label = ttk.Label(master=self.winner_frame, text='Surname')
        self.input_surname = ttk.Entry(master=self.winner_frame, width=40)
        self.surname_label.pack()
        self.input_surname.pack()
        self.middlename_label = ttk.Label(master=self.winner_frame, text='Middlename')
        self.input_middlename = ttk.Entry(master=self.winner_frame, width=40)
        self.middlename_label.pack()
        self.input_middlename.pack()
        self.winner_frame.pack(pady=5)

        self.prize_frame = ttk.Labelframe(self, text="Tournament prize range")
        self.input_minprize = ttk.Entry(master=self.prize_frame)
        self.input_minprize.pack(pady=0, side=tk.LEFT)
        self.input_maxprize = ttk.Entry(master=self.prize_frame)
        self.input_maxprize.pack(padx=0, pady=0, side=tk.LEFT)
        self.prize_frame.pack(pady=5)

        self.winner_prize_frame = ttk.Labelframe(self, text="Winner prize range")
        self.input_minprize_winner = ttk.Entry(master=self.winner_prize_frame)
        self.input_minprize_winner.pack(pady=0, side=tk.LEFT)
        self.input_maxprize_winner = ttk.Entry(master=self.winner_prize_frame)
        self.input_maxprize_winner.pack(padx=0, pady=0, side=tk.LEFT)
        self.winner_prize_frame.pack(pady=5)

        self.tool_frame = ttk.Frame(self)
        self.cancel_button = ttk.Button(master=self.tool_frame, text="Cancel", width=15,  command=self.destroy)
        self.cancel_button.pack(pady=0, side=tk.LEFT)
        self.add_button = ttk.Button(master=self.tool_frame, text="Delete tournaments", command=self.delete)
        self.add_button.pack(padx=5, pady=0, side=tk.LEFT)
        self.tool_frame.pack(pady=10)

        
    def delete(self): 

        if self.input_title.get(): self.app.delete_filter.title = self.input_title.get()
        if self.datepicker.get_date() != "6/4/24": self.app.delete_filter.date = dt.strptime(self.datepicker.get_date(), '%m/%d/%y')
        if self.input_sport.get(): self.app.delete_filter.sport = self.input_sport.get()
        if self.input_name.get(): self.app.delete_filter.winner_name = self.input_name.get()
        if self.input_surname.get(): self.app.delete_filter.winner_surname = self.input_surname.get()
        if self.input_middlename.get(): self.app.delete_filter.winner_middlename = self.input_middlename.get()

        try:
            if self.input_minprize.get(): self.app.delete_filter.prize_range[0] = int(self.input_minprize.get())
            if self.input_maxprize.get(): self.app.delete_filter.prize_range[1] = int(self.input_maxprize.get())
            if self.input_minprize_winner.get(): self.app.delete_filter.winner_prize_range[0] = int(self.input_minprize_winner.get())
            if self.input_maxprize_winner.get(): self.app.delete_filter.winner_prize_range[1] = int(self.input_maxprize_winner.get())
        
        except ValueError: 
            showerror(title="NotIntError", message="Prize must be integer") 
            return

        self.destroy()
        
        self.app.file.delete_tournaments(self.app.delete_filter)
        self.app.update_data()