import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import xml.sax

class BookHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.current_data = ""
        self.name = ""
        self.author = ""
        self.publisher = ""
        self.volumes = ""
        self.edition = ""
        self.total_volumes = ""
        self.records = []

    def startElement(self, tag, attributes):
        self.current_data = tag

    def endElement(self, tag):
        if self.current_data == "name":
            self.name = self.content
        elif self.current_data == "author":
            self.author = self.content
        elif self.current_data == "publisher":
            self.publisher = self.content
        elif self.current_data == "volumes":
            self.volumes = self.content
        elif self.current_data == "edition":
            self.edition = self.content
        elif self.current_data == "total_volumes":
            self.total_volumes = self.content

        if tag == "book":
            self.records.append([
                self.name,
                self.author,
                self.publisher,
                self.volumes,
                self.edition,
                self.total_volumes
            ])
            self.name = ""
            self.author = ""
            self.publisher = ""
            self.volumes = ""
            self.edition = ""
            self.total_volumes = ""
        self.current_data = ""

    def characters(self, content):
        self.content = content


class Model:
    def __init__(self):
        self.records = []
        
    def add_record(self,name, author, publisher, volumes, edition,num_of_tomes):
        t_list=[]
        t_list.append(name)
        t_list.append(author)
        t_list.append(publisher)
        t_list.append(volumes)
        t_list.append(edition)
        t_list.append(num_of_tomes)
        self.records.append(t_list)

    def delete_by_edition(self,min_edition,max_edition):
        self.records = [record for record in self.records if not (min_edition < int(record[4]) < max_edition)]
                
    def get_records(self):
        return self.records
    
    def give_records_info(self):
        name = self.records[-1][0]
        author = self.records[-1][1]
        publisher = self.records[-1][2]
        volumes = self.records[-1][3]
        edition = self.records[-1][4]
        num_of_tomes =self.records[-1][5]
        return name, author, publisher, volumes, edition,num_of_tomes
    
    def delete_by_publisher_and_author(self, publisher, author):
        self.records = [record for record in self.records if not (record[1] == author and record[2] == publisher)]

    def delete_by_book_name(self,book_name):
        self.records = [record for record in self.records if not (record[0] == book_name)]
                
    def delete_by_author(self,author):
        self.records = [record for record in self.records if not (record[1] == author)]


    def delete_by_volumes(self,min_volumes,max_volumes):
        self.records = [record for record in self.records if not (min_volumes < int(record[3]) < max_volumes)]

    def delete_by_total_volumes(self,min_edition, max_edition):
        self.records = [record for record in self.records if not (min_edition < int(record[5]) < max_edition)]
        
    def search_by_author(self, author):
        return [record for record in self.records if record[1] == author]

    def search_by_publisher_and_author(self, publisher, author):
        return [record for record in self.records if record[1] == author and record[2] == publisher]

    def search_by_book_name(self, book_name):
        return [record for record in self.records if record[0] == book_name]

    def search_by_volumes(self, min_volumes, max_volumes):
        return [record for record in self.records if min_volumes <= int(record[3]) <= max_volumes]

    def search_by_edition(self, min_edition, max_edition):
        return [record for record in self.records if min_edition <= int(record[4]) <= max_edition]

    def search_by_total_volumes(self, min_total_volumes, max_total_volumes):
        return [record for record in self.records if min_total_volumes <= int(record[5]) <= max_total_volumes]

    def create_records_from_xml(self, filename):
        handler = BookHandler()
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        try:
            parser.parse(filename)
            self.records = handler.records
            return True
        except FileNotFoundError:
            print("Файл не найден.")
            return False
        except xml.sax.SAXParseException:
            print("Ошибка парсинга XML файла.")
            return False    
