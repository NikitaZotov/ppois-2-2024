
import sys
sys.path.append('D:\\unik\\PPOIS\\Lab2\\')

from model import Model
from view import BookRecord
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import xml.etree.ElementTree as ET

class Controller:
    def __init__(self):
        self.model = Model()
        self.view = BookRecord(self)

    def main(self):
        self.view._main()
    
    def get_record_add_info(self,name, author, publisher, volumes, edition,num_of_tomes):
        self.model.add_record(name, author, publisher, volumes, edition,num_of_tomes)
    
    def add_record(self, record):
        self.model.add_record(record)

    def get_records(self):
        return self.model.get_records()
    
    def delete_by_book_name(self,book_name):
        self.model.delete_by_book_name(book_name)
        
    def delete_by_edition(self,min_edition, max_edition):
        self.model.delete_by_edition(min_edition,max_edition)
    
    def search_records(self, condition):
        return self.model.search_records(condition)

    def delete_records(self, condition):
        self.model.delete_records(condition)

    def delete_by_total_volumes(self,min_edition, max_edition):
        self.model.delete_by_total_volumes(min_edition, max_edition)
    
    def delete_by_author(self,author):
        self.model.delete_by_author(author)
    
    def delete_by_volumes(self,min_volumes,max_volumes):
        self.model.delete_by_volumes(min_volumes,max_volumes)
    
    def delete_by_publisher_and_author(self,publisher, author):
        self.model.delete_by_publisher_and_author(publisher, author)
        
    def give_records_info(self):
        return self.model.give_records_info()
    
    def search_by_author(self, author):
        return self.model.search_by_author(author)

    def search_by_publisher_and_author(self, publisher, author):
        return self.model.search_by_publisher_and_author(publisher, author)

    def search_by_book_name(self, book_name):
        return self.model.search_by_book_name(book_name)

    def search_by_volumes(self, min_volumes, max_volumes):
        return self.model.search_by_volumes(min_volumes, max_volumes)

    def search_by_edition(self, min_edition, max_edition):
        return self.model.search_by_edition(min_edition, max_edition)

    def search_by_total_volumes(self, min_total_volumes, max_total_volumes):
        return self.model.search_by_total_volumes(min_total_volumes, max_total_volumes)

    def load_records_from_xml(self, filename):
        return self.model.create_records_from_xml(filename)
    
if __name__ == "__main__":
    controller = Controller()
    controller.main()

