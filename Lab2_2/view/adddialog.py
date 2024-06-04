from datetime import datetime as dt


import tkinter as tk
from tkinter.messagebox import showwarning, showerror
from tkinter import ttk

from tkcalendar import Calendar
from ttkthemes import ThemedStyle

from model.winner import Winner


class AddDialog(tk.Toplevel):

    def __init__(self, master, app):
        super().__init__(master=master)
        self.app = app
        self.minsize(height=400, width=300)
        self['bg'] = 'gray22'
        self.theme = ThemedStyle(master=self)
        self.theme.set_theme('black')
        self.title("Add tournament")

        self.title_frame = ttk.Labelframe(self, text="Tournament title")
        self.input_title = ttk.Entry(master=self.title_frame, width=40)
        self.input_title.pack()
        self.title_frame.pack(pady=5)

        self.sport_frame = ttk.Labelframe(self, text="Tournament sport")
        self.input_sport = ttk.Entry(master=self.sport_frame, width=40)
        self.input_sport.pack()
        self.sport_frame.pack(pady=5)

        self.prize_frame = ttk.Labelframe(self, text="Tournament prize")
        self.input_prize = ttk.Entry(master=self.prize_frame, width=40)
        self.input_prize.pack()
        self.prize_frame.pack(pady=5)

        self.datepicker_frame = ttk.LabelFrame(self, text="Tournament date")
        self.datepicker = Calendar(master=self.datepicker_frame, year=dt.now().year, 
                                   month=dt.now().month, day=dt.now().day)
        
        self.datepicker.pack()
        self.datepicker_frame.pack()

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

        self.tool_frame = ttk.Frame(self)
        self.cancel_button = ttk.Button(master=self.tool_frame, text="Cancel", width=15,  command=self.destroy)
        self.cancel_button.pack(pady=0, side=tk.LEFT)
        self.add_button = ttk.Button(master=self.tool_frame, text="Add tournament", command=self.add)
        self.add_button.pack(padx=5, pady=0, side=tk.LEFT)
        self.tool_frame.pack(pady=10)

        
    def add(self):

        if all((self.input_title.get(), self.datepicker.get_date(), self.input_sport.get(),
                self.input_name.get(), self.input_surname.get(), self.input_middlename.get(),
                self.input_prize.get())):
            
            try:
                self.app.file.add_tournament(self.input_title.get(), dt.strptime(self.datepicker.get_date(), '%m/%d/%y'), self.input_sport.get(), 
                                             Winner(self.input_name.get(), self.input_surname.get(), self.input_middlename.get()),
                                             int(self.input_prize.get()))
                
            except ValueError: 
                showerror(title="NotIntError", message="Tournament prize must be integer")
                return
            
            self.app.update_data()
        
        else: showwarning(title="Warning", message="Not all fields are filled")







        
        



        

