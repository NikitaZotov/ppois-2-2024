import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class MainView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.controller = None
        self.title("Student Records")
        
        self.create_menu()
        self.create_toolbar()
        self.create_table()
        self.create_pagination_controls()
    
    def set_controller(self, controller):
        self.controller = controller
    
    def create_menu(self):
        menu_bar = tk.Menu(self)
        
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Load", command=lambda: self.controller.load_records())
        file_menu.add_command(label="Save", command=lambda: self.controller.save_records())
        menu_bar.add_cascade(label="File", menu=file_menu)
        
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Add Record", command=lambda: self.controller.show_add_record_dialog())
        edit_menu.add_command(label="Search Records", command=lambda: self.controller.show_search_record_dialog())
        edit_menu.add_command(label="Delete Records", command=lambda: self.controller.show_delete_record_dialog())
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        
        self.config(menu=menu_bar)
    
    def create_toolbar(self):
        toolbar = tk.Frame(self, bd=1)
        
        add_record_btn = tk.Button(toolbar, text="Add Record", command=lambda: self.controller.show_add_record_dialog())
        add_record_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        search_record_btn = tk.Button(toolbar, text="Search Records", command=lambda: self.controller.show_search_record_dialog())
        search_record_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        delete_record_btn = tk.Button(toolbar, text="Delete Records", command=lambda: self.controller.show_delete_record_dialog())
        delete_record_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        toolbar.pack(side=tk.TOP, fill=tk.X)

    def create_table(self):
        self.tree = ttk.Treeview(self, columns=("Student Name", "Father Name", "Father Income", "Mother Name", "Mother Income", "Brothers", "Sisters"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(expand=True, fill=tk.BOTH)
    
    def create_pagination_controls(self):
        pagination_frame = tk.Frame(self)
        
        self.page_info = tk.Label(pagination_frame, text="Page 1 of 1")
        self.page_info.pack(side=tk.LEFT)
        
        self.first_btn = tk.Button(pagination_frame, text="First", command=lambda: self.controller.first_page())
        self.first_btn.pack(side=tk.LEFT)
        
        self.prev_btn = tk.Button(pagination_frame, text="Previous", command=lambda: self.controller.prev_page())
        self.prev_btn.pack(side=tk.LEFT)
        
        self.next_btn = tk.Button(pagination_frame, text="Next", command=lambda: self.controller.next_page())
        self.next_btn.pack(side=tk.LEFT)
        
        self.last_btn = tk.Button(pagination_frame, text="Last", command=lambda: self.controller.last_page())
        self.last_btn.pack(side=tk.LEFT)
        
        pagination_frame.pack(side=tk.BOTTOM, fill=tk.X)

    def update_table(self, records):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        for record in records:
            self.tree.insert("", tk.END, values=(record.student_name, record.father_name, record.father_income, record.mother_name, record.mother_income, record.num_brothers, record.num_sisters))
        
    def update_pagination_info(self, current_page, total_pages):
        self.page_info.config(text=f"Page {current_page} of {total_pages}")
    
    def show_message(self, message):
        messagebox.showinfo("Information", message)

class RecordDialog(tk.Toplevel):
    def __init__(self, parent, controller, title):
        super().__init__(parent)
        self.controller = controller
        self.title(title)
        
        self.create_widgets()
        
    def create_widgets(self):
        fields = ["Student Name", "Father Name", "Father Income", "Mother Name", "Mother Income", "Number of Brothers", "Number of Sisters"]
        self.entries = {}
        
        for field in fields:
            frame = tk.Frame(self)
            label = tk.Label(frame, text=field)
            entry = tk.Entry(frame)
            
            label.pack(side=tk.LEFT)
            entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)
            
            frame.pack(fill=tk.X, padx=5, pady=5)
            self.entries[field] = entry
        
        self.ok_button = tk.Button(self, text="OK", command=self.on_ok)
        self.ok_button.pack(pady=5)
    
    def on_ok(self):
        data = {field: entry.get() for field, entry in self.entries.items()}
        self.controller.on_record_dialog_ok(data)
        self.destroy()

class SearchDialog(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title("Search Records")
        
        self.create_widgets()
        
    def create_widgets(self):
        fields = [
            "Student Name", "Father Name", "Father Income (Min)", "Father Income (Max)", 
            "Mother Name", "Mother Income (Min)", "Mother Income (Max)", 
            "Number of Brothers", "Number of Sisters"
        ]
        self.entries = {}
        
        for field in fields:
            frame = tk.Frame(self)
            label = tk.Label(frame, text=field)
            entry = tk.Entry(frame)
            
            label.pack(side=tk.LEFT)
            entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)
            
            frame.pack(fill=tk.X, padx=5, pady=5)
            self.entries[field] = entry
        
        self.ok_button = tk.Button(self, text="OK", command=self.on_ok)
        self.ok_button.pack(pady=5)

    def on_ok(self):
        criteria = {
            "student_name": self.entries["Student Name"].get(),
            "father_name": self.entries["Father Name"].get(),
            "mother_name": self.entries["Mother Name"].get(),
            "num_brothers": int(self.entries["Number of Brothers"].get()) if self.entries["Number of Brothers"].get() else None,
            "num_sisters": int(self.entries["Number of Sisters"].get()) if self.entries["Number of Sisters"].get() else None,
            "father_income_min": float(self.entries["Father Income (Min)"].get()) if self.entries["Father Income (Min)"].get() else None,
            "father_income_max": float(self.entries["Father Income (Max)"].get()) if self.entries["Father Income (Max)"].get() else None,
            "mother_income_min": float(self.entries["Mother Income (Min)"].get()) if self.entries["Mother Income (Min)"].get() else None,
            "mother_income_max": float(self.entries["Mother Income (Max)"].get()) if self.entries["Mother Income (Max)"].get() else None,
        }
        self.controller.on_search_dialog_ok(criteria)
        self.destroy()


class DeleteDialog(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title("Delete Records")
        
        self.create_widgets()
        
    def create_widgets(self):
        fields = [
            "Student Name", "Father Name", "Father Income (Min)", "Father Income (Max)", 
            "Mother Name", "Mother Income (Min)", "Mother Income (Max)", 
            "Number of Brothers", "Number of Sisters"
        ]
        self.entries = {}
        
        for field in fields:
            frame = tk.Frame(self)
            label = tk.Label(frame, text=field)
            entry = tk.Entry(frame)
            
            label.pack(side=tk.LEFT)
            entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)
            
            frame.pack(fill=tk.X, padx=5, pady=5)
            self.entries[field] = entry
        
        self.ok_button = tk.Button(self, text="OK", command=self.on_ok)
        self.ok_button.pack(pady=5)

    def on_ok(self):
        criteria = {
            "student_name": self.entries["Student Name"].get(),
            "father_name": self.entries["Father Name"].get(),
            "mother_name": self.entries["Mother Name"].get(),
            "num_brothers": int(self.entries["Number of Brothers"].get()) if self.entries["Number of Brothers"].get() else None,
            "num_sisters": int(self.entries["Number of Sisters"].get()) if self.entries["Number of Sisters"].get() else None,
            "father_income_min": float(self.entries["Father Income (Min)"].get()) if self.entries["Father Income (Min)"].get() else None,
            "father_income_max": float(self.entries["Father Income (Max)"].get()) if self.entries["Father Income (Max)"].get() else None,
            "mother_income_min": float(self.entries["Mother Income (Min)"].get()) if self.entries["Mother Income (Min)"].get() else None,
            "mother_income_max": float(self.entries["Mother Income (Max)"].get()) if self.entries["Mother Income (Max)"].get() else None,
        }
        self.controller.on_delete_dialog_ok(criteria)
        self.destroy()

class SearchResultsView(tk.Toplevel):
    def __init__(self, parent, controller, results):
        super().__init__(parent)
        self.controller = controller
        self.results = results
        self.current_page = 1
        self.records_per_page = 15
        self.total_pages = (len(self.results) + self.records_per_page - 1) // self.records_per_page
        
        self.title("Search Results")
        
        self.create_table()
        self.create_pagination_controls()
        self.update_table()
        self.update_pagination_info()
    
    def create_table(self):
        self.tree = ttk.Treeview(self, columns=("Student Name", "Father Name", "Father Income", "Mother Name", "Mother Income", "Brothers", "Sisters"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(expand=True, fill=tk.BOTH)
    
    def create_pagination_controls(self):
        pagination_frame = tk.Frame(self)
        
        self.page_info = tk.Label(pagination_frame, text=f"Page 1 of {self.total_pages}")
        self.page_info.pack(side=tk.LEFT)
        
        self.first_btn = tk.Button(pagination_frame, text="First", command=self.first_page)
        self.first_btn.pack(side=tk.LEFT)
        
        self.prev_btn = tk.Button(pagination_frame, text="Previous", command=self.prev_page)
        self.prev_btn.pack(side=tk.LEFT)
        
        self.next_btn = tk.Button(pagination_frame, text="Next", command=self.next_page)
        self.next_btn.pack(side=tk.LEFT)
        
        self.last_btn = tk.Button(pagination_frame, text="Last", command=self.last_page)
        self.last_btn.pack(side=tk.LEFT)
        
        pagination_frame.pack(side=tk.BOTTOM, fill=tk.X)
    
    def update_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        start_index = (self.current_page - 1) * self.records_per_page
        end_index = start_index + self.records_per_page
        records = self.results[start_index:end_index]
        
        for record in records:
            self.tree.insert("", tk.END, values=(record.student_name, record.father_name, record.father_income, record.mother_name, record.mother_income, record.num_brothers, record.num_sisters))
        
    def update_pagination_info(self):
        self.page_info.config(text=f"Page {self.current_page} of {self.total_pages}")
    
    def first_page(self):
        if self.current_page != 1:
            self.current_page = 1
            self.update_table()
            self.update_pagination_info()
    
    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_table()
            self.update_pagination_info()
    
    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.update_table()
            self.update_pagination_info()
            
    def last_page(self):
        if self.current_page != self.total_pages:
            self.current_page = self.total_pages
            self.update_table()
            self.update_pagination_info()
