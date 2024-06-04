import tkinter as tk
from tkinter import filedialog
import xml.etree.ElementTree as ET

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("XML File Creator")
        self.geometry("300x200")
        self.create_widgets()

    def create_widgets(self):
        # Создание меню
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # Добавление пункта меню "Файл"
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)

        # Добавление команды "Создать новый XML файл" в меню "Файл"
        file_menu.add_command(label="Создать новый XML файл", command=self.create_new_xml_file)

    def create_new_xml_file(self):
        # Запрос пути для сохранения нового XML файла
        file_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
        if file_path:
            # Создание структуры XML
            root = ET.Element("pet_records")
            tree = ET.ElementTree(root)
            # Сохранение в файл
            tree.write(file_path, encoding="utf-8", xml_declaration=True)
            tk.messagebox.showinfo("Успех", f"Файл успешно создан: {file_path}")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
