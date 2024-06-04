from view.CenteredWindowHelper import center_window

import tkinter as tk
from tkinter import ttk, filedialog


class CreateFileWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Create File")
        center_window(self, 230, 130)
        self.minsize(width=230, height=130)

        # Create widgets
        ttk.Label(self, text="File Type: xml").pack(pady=10)
        self.file_type_var = tk.StringVar()
        self.filename = ""

        ttk.Label(self, text="File Name:").pack()
        self.file_name_entry = ttk.Entry(self)
        self.file_name_entry.insert(0, "teams")
        self.file_name_entry.pack()

        ttk.Button(self, text="Create", command=self.create_file).pack(pady=10)

    def show(self):
        self.grab_set()
        self.wait_window()
        return self.filename

    def create_file(self):
        file_type = self.file_type_var.get()
        file_name = self.file_name_entry.get()

        filetypes = [('XML files', '*.xml')]
        self.filename = filedialog.asksaveasfilename(defaultextension=file_type,
                                                     initialfile=file_name,
                                                     filetypes=filetypes)
        if self.filename:
            with open(self.filename, 'w') as f:
                pass
            print(f"File '{self.filename}' created.")
            self.destroy()
