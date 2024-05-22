import xml.dom.minidom as dom
import xml.sax
from xml.sax import make_parser
import re

class Paginator:
    def __init__(self, items, items_per_page=10):
        self.items = items
        self.current_page = 1
        self.items_per_page = items_per_page
        self.total_pages = max(1, (len(items) - 1) // items_per_page + 1)
        self.update_pagination()

    def update_pagination(self):
        self.total_pages = max(1, -(-len(self.items) // self.items_per_page))
        self.current_page = max(1, min(self.current_page,self.total_pages))

    def set_items_per_page(self, items_per_page):
        self.items_per_page = items_per_page
        self.update_pagination()

    def get_page_items(self):
        if self.current_page < self.total_pages:
            start = (self.current_page - 1) * self.items_per_page
            end = start + self.items_per_page
            return self.items[start:end]
        else:
            start = (self.current_page - 1) * self.items_per_page
            return self.items[start:]

    def go_to_first_page(self):
        self.current_page = 1

    def go_to_last_page(self):
        self.current_page = self.total_pages

    def go_to_next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1

    def go_to_previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1

class ClientsHandler(xml.sax.ContentHandler):
    def __init__(self, model):
        self.model = model
        self.current_data = ""
        self.client_info = {}

    def startElement(self, tag, attributes):
        self.current_data = tag
        if tag == "client":
            self.client_info = {}

    def endElement(self, tag):
        if tag == "client":
            self.model.add_client(self.client_info)
            self.client_info = {}
        self.current_data = ""

    def characters(self, content):
        if self.current_data in ["full_name", "account_number", "address", "mobile_phone", "landline_phone"]:
            self.client_info[self.current_data] = content

class ClientModel:
    def __init__(self, clients_per_page = 10):
        self.clients_list = []
        self.paginator = Paginator(self.clients_list)
        self.clients_per_page = clients_per_page
        self.current_page = 1
        self.total_pages = max(1, (len(self.clients_list) - 1) // self.clients_per_page + 1)

    def add_client(self, client_info):
        self.clients_list.append(client_info)

    def save_to_xml_dom(self, filepath):
        # Создание XML-документа и корневого элемента
        impl = dom.getDOMImplementation()
        newdoc = impl.createDocument(None, "clients", None)
        root_node = newdoc.documentElement

        # Добавление клиентов в XML
        for client in self.clients_list:
            client_node = newdoc.createElement('client')
            for key, value in client.items():
                element = newdoc.createElement(key)
                element.appendChild(newdoc.createTextNode(str(value)))
                client_node.appendChild(element)
            root_node.appendChild(client_node)

        # Сохранение XML-файла
        with open(filepath, 'w') as xml_file:
            newdoc.writexml(xml_file)

    def load_clients_from_xml(self, filepath):
        handler = ClientsHandler(self)
        parser = make_parser()
        parser.setContentHandler(handler)


        with open(filepath, 'r') as file:
            parser.parse(file)

    def search_clients(self, phone=None, surname=None, account_number=None, address=None, full_name=None):
        filtered_clients = []
        for client in self.clients_list:
            if phone and (phone in client.get('mobile_phone') or phone in client.get('landline_phone')):
                filtered_clients.append(client)
            elif surname and surname.lower() in client.get('full_name', '').lower():
                filtered_clients.append(client)
            elif account_number and account_number == client.get('account_number'):
                filtered_clients.append(client)
            elif address and address.lower() in client.get('address', '').lower():
                filtered_clients.append(client)
            elif full_name:
                parts = full_name.split()
                name_matches = [part.lower() in client.get('full_name', '').lower() for part in parts if part]
                if any(name_matches) and any(
                        part in client.get('mobile_phone') or part in client.get('landline_phone') for part in parts if
                        part.isdigit()):
                    filtered_clients.append(client)
        return filtered_clients

    def delete_client(self, query):
        query = query.lower()
        new_clients_list = []
        client_removed = False
        for client in self.clients_list:
            if query not in client.get('last_name', '').lower() and \
               query not in client.get('phone', '').lower() and \
               query not in client.get('account_number', '').lower() and \
               query not in client.get('address', '').lower() and \
               not any(query in value.lower() for key, value in client.items() if 'name' in key):
                new_clients_list.append(client)
            else:
                client_removed = True

        self.clients_list = new_clients_list
        return client_removed

    def get_page_items(self):
        if self.current_page < self.total_pages:
            start = (self.current_page - 1) * self.clients_per_page
            end = start + self.clients_per_page
            return self.clients_list[start:end]
        else:
            start = (self.current_page - 1) * self.clients_per_page
            return self.clients_list[start:]

    def go_to_first_page(self):
        self.update_data()
        self.current_page = 1

    def go_to_last_page(self):
        self.update_data()
        self.current_page = self.total_pages

    def go_to_next_page(self):
        self.update_data()
        if self.current_page < self.total_pages:
            self.current_page += 1

    def go_to_previous_page(self):
        self.update_data()
        if self.current_page > 1:
            self.current_page -= 1
    def get_page_data(self, page=None):
        # if page is not None:
        #     self.current_page = page
        if self.current_page < self.total_pages:
            start = (self.current_page-1) * self.clients_per_page
            end = start + self.clients_per_page
            return self.clients_list[start:end]
        else:
            start = (self.current_page-1) * self.clients_per_page
            return self.clients_list[start:]

    def update_data(self):
        if len(self.clients_list) % 2 == 0:
            self.total_pages = (len(self.clients_list) // self.clients_per_page)
        else:
            self.total_pages = (len(self.clients_list) // self.clients_per_page) + 1

    def set_items_per_page(self, clients_per_page):
        self.clients_per_page = clients_per_page
        self.total_pages = max(1, (len(self.clients_list) - 1) // clients_per_page + 1)
        self.current_page = min(self.current_page, self.total_pages)
        self.update_data()
