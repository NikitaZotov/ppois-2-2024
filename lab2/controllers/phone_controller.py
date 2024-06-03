import math
import os
import xml.sax
from models.phone import Phone


class PhoneController:
    def __init__(self):
        self.phone_list = []
        self.rec_per_page = 10
        self.current_page = 1
        self.total_pages = 1

    def add_phone(self, phone):
        self.phone_list.append(phone)
        self.update_total_pages()

    def delete_phone(self, delete_type, query):
        indices_to_delete = []
        for i, phone in enumerate(self.phone_list):
            if delete_type == "ФИО клиента или номер телефона" and (query.lower() in phone.full_name.lower() or query in phone.mobile or query in phone.landline):
                indices_to_delete.append(i)
            elif delete_type == "Номер счета или адрес" and (query == phone.account_number or query.lower() in phone.address.lower()):
                indices_to_delete.append(i)
            elif delete_type == "ФИО клиента и цифры в номере" and (query.lower() in phone.full_name.lower() or any(char.isdigit() for char in query) and (query in phone.mobile or query in phone.landline)):
                indices_to_delete.append(i)

        for index in reversed(indices_to_delete):
            del self.phone_list[index]

    def search_phone(self, search_type, query):
        results = []
        for phone in self.phone_list:
            if search_type == "ФИО клиента или номер телефона" and (query.lower() in phone.full_name.lower() or query in phone.mobile or query in phone.landline):
                results.append(phone)
            elif search_type == "Номер счета или адрес" and (query == phone.account_number or query.lower() in phone.address.lower()):
                results.append(phone)
            elif search_type == "ФИО клиента и цифры в номере" and (query.lower() in phone.full_name.lower() or any(char.isdigit() for char in query) and (query in phone.mobile or query in phone.landline)):
                results.append(phone)
        return results

    def update_total_pages(self):
        self.total_pages = math.ceil(len(self.phone_list) / self.rec_per_page)

    def get_phones_for_page(self):
        start_index = (self.current_page - 1) * self.rec_per_page
        end_index = self.current_page * self.rec_per_page
        return self.phone_list[start_index:end_index]

    def save_data(self, file_path):
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("<Phones>\n")
            for phone in self.phone_list:
                file.write(f"  <Phone>\n")
                file.write(f"    <FullName>{phone.full_name}</FullName>\n")
                file.write(f"    <AccountNumber>{phone.account_number}</AccountNumber>\n")
                file.write(f"    <Address>{phone.address}</Address>\n")
                file.write(f"    <Mobile>{phone.mobile}</Mobile>\n")
                file.write(f"    <Landline>{phone.landline}</Landline>\n")
                file.write(f"  </Phone>\n")
            file.write("</Phones>\n")

    def load_data(self, file_path):
        class PhoneHandler(xml.sax.ContentHandler):
            def __init__(self):
                self.current_element = ""
                self.full_name = ""
                self.account_number = ""
                self.address = ""
                self.mobile = ""
                self.landline = ""
                self.phone_list = []

            def startElement(self, name, attrs):
                self.current_element = name

            def characters(self, content):
                if self.current_element == "FullName":
                    self.full_name += content.strip()
                elif self.current_element == "AccountNumber":
                    self.account_number += content.strip()
                elif self.current_element == "Address":
                    self.address += content.strip()
                elif self.current_element == "Mobile":
                    self.mobile += content.strip()
                elif self.current_element == "Landline":
                    self.landline += content.strip()

            def endElement(self, name):
                if name == "Phone":
                    phone = Phone(self.full_name, self.account_number, self.address, self.mobile, self.landline)
                    self.phone_list.append(phone)
                    self.full_name = ""
                    self.account_number = ""
                    self.address = ""
                    self.mobile = ""
                    self.landline = ""

        handler = PhoneHandler()
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        parser.parse(file_path)
        self.phone_list = handler.phone_list
        self.update_total_pages()
