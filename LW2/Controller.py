from View import *
from Model import *

def is_correct(string):
    for c in string:
        if c.isalpha() or c == " ":
            continue
        else: 
            return False
    return True

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.current_page = 1
        self.records_per_page = 10
        self.total_pages = 1
        
        self.update_view()
        
    def update_view(self):
        start_index = (self.current_page - 1) * self.records_per_page
        end_index = start_index + self.records_per_page
        records = self.model.records[start_index:end_index]
        self.view.update_table(records)
        
        self.total_pages = (len(self.model.records) + self.records_per_page - 1) // self.records_per_page
        self.view.update_pagination_info(self.current_page, self.total_pages)
    
    def show_add_record_dialog(self):
        RecordDialog(self.view, self, "Add Record")
    
    def show_search_record_dialog(self):
        SearchDialog(self.view, self)
    
    def show_delete_record_dialog(self):
        DeleteDialog(self.view, self)
    
    def on_record_dialog_ok(self, data):
        try:
            student_name = str(data["Student Name"])
            if not is_correct(student_name):
                raise ValueError("Invalid input")
            father_name = str(data["Father Name"])
            if not is_correct(father_name):
                raise ValueError("Invalid input")
            mother_name = str(data["Mother Name"])
            if not is_correct(mother_name):
                raise ValueError("Invalid input")
            father_income = float(data["Father Income"])
            mother_income = float(data["Mother Income"])
            num_brothers = int(data["Number of Brothers"])
            num_sisters = int(data["Number of Sisters"])

            record = Record(student_name, father_name, father_income, mother_name, mother_income, num_brothers, num_sisters)
            self.model.add_record(record)
            self.update_view()
        except ValueError as ve:
            messagebox.showerror("Invalid input", str(ve))
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def load_records(self):
        file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if file_path:
            self.model.load_from_file(file_path)
            self.update_view()
    
    def save_records(self):
        file_path = filedialog.asksaveasfilename(filetypes=[("XML files", "*.xml")])
        if file_path:
            self.model.save_to_file(file_path)
    
    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_view()
    
    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.update_view()
            
    def first_page(self):
        if self.current_page != 1:
            self.current_page = 1
            self.update_view()
        
    def last_page(self):
        if self.current_page != self.total_pages:
            self.current_page = self.total_pages
            self.update_view()
    
    def on_search_dialog_ok(self, criteria):
        results = self.model.search_records(criteria)
        self.view.update_table(results)
        self.view.show_message(f"Found {len(results)} record(s) matching criteria.")

    def on_delete_dialog_ok(self, criteria):
        deleted_count = self.model.delete_records(criteria)
        self.update_view()
        self.view.show_message(f"Deleted {deleted_count} record(s).")

