import tkinter as tk
from tkinter import ttk, filedialog
from xml.dom.minidom import Document
import xml.sax
from controllers.sportsman_controller import *
from views.sportsman_view import create_labels_and_entries, create_treeview
from views.sportsman_table_view import update_table, navigate_page

# Creating main window
window = tk.Tk()
window.title("Таблица спортсменов")

labels = ["ФИО спортсмена", "Состав", "Позиция", "Титулы", "Вид спорта", "Разряд"]
entries = create_labels_and_entries(window, labels)
tree = create_treeview(window, labels)

page_label = tk.Label(window, text="")
page_label.grid(row=len(labels) + 2, column=2, pady=5)

nav_frame = tk.Frame(window)
nav_frame.grid(row=len(labels) + 3, column=2, columnspan=4)

first_button = tk.Button(nav_frame, text="<<", command=lambda: navigate_page(tree, page_label, 1))
first_button.grid(row=0, column=0, pady=5)

previous_button = tk.Button(nav_frame, text="<", command=lambda: navigate_page(tree, page_label, current_page - 1))
previous_button.grid(row=0, column=1, pady=5)

next_button = tk.Button(nav_frame, text=">", command=lambda: navigate_page(tree, page_label, current_page + 1))
next_button.grid(row=0, column=2, pady=5)

last_button = tk.Button(nav_frame, text=">>", command=lambda: navigate_page(tree, page_label, total_pages))
last_button.grid(row=0, column=3, pady=5)

entry_full_name, entry_team, entry_position, entry_titles, entry_sport_type, entry_rank = entries

def add_to_table():
    values = [
        entry_full_name.get(),
        entry_team.get(),
        entry_position.get(),
        entry_titles.get(),
        entry_sport_type.get(),
        entry_rank.get()
    ]
    if all(values):
        add_sportsman(*values)
        clear_entries()
        update_table(tree, page_label)

def clear_entries():
    for entry in entries:
        entry.delete(0, tk.END)

add_button = tk.Button(window, text="Добавить", command=add_to_table)
add_button.grid(row=len(labels), column=0, columnspan=2, pady=10)

selected_search_type = tk.StringVar()
search_tree = ttk.Treeview()

def open_search_dialog():
    global search_tree

    search_dialog = tk.Toplevel(window)
    search_dialog.title("Поиск")
    search_type_label = tk.Label(search_dialog, text="Тип поиска:")
    search_type_label.pack(padx=10, pady=5)
    search_type_combobox = ttk.Combobox(search_dialog,
                                        values=["ФИО или Вид спорта", "Количество титулов", "ФИО или Разряд"],
                                        textvariable=selected_search_type)
    search_type_combobox.pack(pady=5)

    search_entry = tk.Entry(search_dialog)
    search_entry.pack(padx=10, pady=5)

    search_button = tk.Button(search_dialog, text="Искать",
                              command=lambda: perform_search(search_type_combobox.get(), search_entry.get()))
    search_button.pack(pady=10)

    search_tree = ttk.Treeview(search_dialog, columns=labels, show='headings')
    for label in labels:
        search_tree.heading(label, text=label)
    search_tree.pack(side=tk.RIGHT, padx=10, pady=5)



def perform_search(search_type, query):
    for item in search_tree.get_children():
        search_tree.delete(item)

    results = search_sportsmen(search_type, query)
    for sportsman in results:
        search_tree.insert('', 'end', values=[
            sportsman.full_name, sportsman.team, sportsman.position,
            sportsman.titles, sportsman.sport_type, sportsman.rank
        ])

search_button = tk.Button(window, text="Поиск", command=open_search_dialog)
search_button.grid(row=len(labels), column=1, pady=10)

menu_bar = tk.Menu(window)

def open_delete_dialog():
    global search_tree

    delete_dialog = tk.Toplevel(window)
    delete_dialog.title("Удаление")
    delete_type_label = tk.Label(delete_dialog, text="Тип удаления:")
    delete_type_label.pack(padx=10, pady=5)
    delete_type_combobox = ttk.Combobox(delete_dialog,
                                        values=["ФИО или Вид спорта", "Количество титулов", "ФИО или Разряд"],
                                        textvariable=selected_search_type)
    delete_type_combobox.pack(pady=5)

    delete_entry = tk.Entry(delete_dialog)
    delete_entry.pack(padx=10, pady=5)

    delete_button = tk.Button(delete_dialog, text="Удалить",
                              command=lambda: perform_delete(selected_search_type.get(), delete_entry.get(), delete_counter_label))
    delete_button.pack(pady=10)

    delete_counter_label = tk.Label(delete_dialog, text="Удалено: 0")
    delete_counter_label.pack(padx=10, pady=5)

def perform_delete(delete_type, query, delete_counter_label):
    global sportsman_list

    indices_to_delete = []

    for i, sportsman in enumerate(sportsman_list):
        if delete_type == "ФИО или Вид спорта" and (query.lower() in sportsman.full_name.lower() or query.lower() in sportsman.sport_type.lower()):
            indices_to_delete.append(i)
        elif delete_type == "Количество титулов" and sportsman.titles == int(query):
            indices_to_delete.append(i)
        elif delete_type == "ФИО или Разряд" and (query.lower() in sportsman.full_name.lower() or query.lower() in sportsman.rank.lower()):
            indices_to_delete.append(i)

    delete_counter_label.config(text=f"Удалено: {len(indices_to_delete)}")

    for index in reversed(indices_to_delete):
        children = tree.get_children()
        if index < len(children):
            tree.delete(children[index])
            del sportsman_list[index]


delete_button = tk.Button(window, text="Удалить", command=open_delete_dialog)
delete_button.grid(row=len(labels) + 1, column=0, columnspan=2, pady=10)

def save_data():
    doc = Document()
    sportsmen_element = doc.createElement("Sportsmen")
    doc.appendChild(sportsmen_element)
    for sportsman in sportsman_list:
        sportsman_element = doc.createElement("Sportsman")
        for attribute_name in ["full_name", "team", "position", "titles", "sport_type", "rank"]:
            attribute_element = doc.createElement(attribute_name)
            attribute_element.appendChild(doc.createTextNode(str(getattr(sportsman, attribute_name))))
            sportsman_element.appendChild(attribute_element)
        sportsmen_element.appendChild(sportsman_element)
    file_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
    with open(file_path, "w", encoding="utf-8") as file:
        doc.writexml(file, indent="  ", addindent="  ", newl="\n")

def load_data():
    global sportsman_list
    file_path = filedialog.askopenfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
    if not file_path:
        return
    class SportsmanHandler(xml.sax.ContentHandler):
        def __init__(self):
            self.current_sportsman = None
            self.current_element = None
        def startElement(self, name, attrs):
            self.current_element = name
            if name == "Sportsman":
                self.current_sportsman = Sportsman("", "", "", "", "", "")
        def characters(self, content):
            if self.current_sportsman and self.current_element:
                setattr(self.current_sportsman, self.current_element, content)
        def endElement(self, name):
            self.current_element = None
            if name == "Sportsman" and self.current_sportsman:
                sportsman_list.append(self.current_sportsman)
    handler = SportsmanHandler()
    parser = xml.sax.make_parser()
    parser.setContentHandler(handler)
    parser.parse(file_path)
    update_table(tree, page_label)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Сохранить", command=save_data)
file_menu.add_command(label="Загрузить", command=load_data)
menu_bar.add_cascade(label="Файл", menu=file_menu)
window.config(menu=menu_bar)

window.mainloop()
