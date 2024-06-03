import tkinter as tk
from tkinter import filedialog
from controllers.phone_controller import PhoneController
from view.phone_view import PhoneView
from view.phone_table_view import PhoneTableView


def save_data(controller):
    file_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
    if file_path:
        controller.save_data(file_path)


def load_data(controller, table_view):
    file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
    if file_path:
        controller.load_data(file_path)
        table_view.update_table()


if __name__ == "__main__":
    window = tk.Tk()
    window.title("Phone Management System")

    controller = PhoneController()
    table_view = PhoneTableView(window, controller)
    view = PhoneView(window, controller, table_view)

    menu_bar = tk.Menu(window)
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Сохранить", command=lambda: save_data(controller))
    file_menu.add_command(label="Загрузить", command=lambda: load_data(controller, table_view))
    menu_bar.add_cascade(label="Файл", menu=file_menu)
    window.config(menu=menu_bar)

    window.mainloop()
