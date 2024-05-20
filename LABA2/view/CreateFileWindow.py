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
        ttk.Label(self, text="File Type:").pack()
        self.file_type_var = tk.StringVar()
        self.file_type_combobox = ttk.Combobox(self, textvariable=self.file_type_var, state="readonly")
        self.file_type_combobox['values'] = ('.xml',)
        self.file_type_combobox.set('.db')
        self.file_type_combobox.pack()
        self.filename = ""

        self.file_type_var.trace('w', self.update_file_types)

        ttk.Label(self, text="File Name:").pack()
        self.file_name_entry = ttk.Entry(self)
        self.file_name_entry.insert(0, "athletes")
        self.file_name_entry.pack()

        ttk.Button(self, text="Create", command=self.create_file).pack(pady=10)

    def update_file_types(self, *args):
        selected_type = self.file_type_var.get()
        if selected_type == '.db':
            self.file_type_combobox['values'] = ('.xml',)
        elif selected_type == '.xml':
            self.file_type_combobox['values'] = ('.db',)

    def show(self):
        self.grab_set()
        self.wait_window()
        return self.filename

    def create_file(self):
        file_type = self.file_type_var.get()
        file_name = self.file_name_entry.get()

        if file_type and file_name:
            if file_type == '.xml':
                filetypes = [('XML files', '*.xml')]
            else:
                filetypes = [('DB files', '*.db')]
            self.filename = filedialog.asksaveasfilename(defaultextension=file_type,
                                                         initialfile=file_name,
                                                         filetypes=filetypes)
            if self.filename:
                with open(self.filename, 'w') as f:
                    pass
                print(f"File '{self.filename}' created.")
                self.destroy()
