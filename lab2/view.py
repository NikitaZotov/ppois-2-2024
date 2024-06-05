import tkinter as tk
from tkinter import simpledialog, ttk, messagebox


class View:
    def __init__(self, root):
        self.root = root
        self.root.title("Учет товаров на складе")
        self.create_widgets()

    def create_widgets(self):
        self.tool_frame = tk.Frame(self.root)  # Создаем как атрибут класса для доступа к нему из контроллера
        self.tool_frame.pack(side=tk.TOP, fill=tk.X)

        self.load_button = tk.Button(self.tool_frame, text="Загрузить файл")
        self.load_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.save_button = tk.Button(self.tool_frame, text="Сохранить файл")
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.add_button = tk.Button(self.tool_frame, text="Добавить продукт")
        self.add_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.search_button = tk.Button(self.tool_frame, text="Поиск")
        self.search_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.delete_button = tk.Button(self.tool_frame, text="Удаление")
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.tree = ttk.Treeview(self.root, columns=("Название товара", "Название производителя", "УНП производителя", "Количество", "Адрес склада"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Панель для управления страницами
        self.page_control_frame = tk.Frame(self.root)
        self.page_control_frame.pack(side=tk.TOP, fill=tk.X)

        tk.Label(self.page_control_frame, text="Элементов на странице:").pack(side=tk.LEFT, padx=5)
        self.items_per_page_combobox = ttk.Combobox(self.page_control_frame, values=[5, 10, 20, 50, 100], state="readonly")
        self.items_per_page_combobox.current(1)  # По умолчанию выбираем 10 элементов на странице
        self.items_per_page_combobox.pack(side=tk.LEFT, padx=5)

        self.prev_button = tk.Button(self.page_control_frame, text="Предыдущая", command=self.prev_page)
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.next_button = tk.Button(self.page_control_frame, text="Следующая", command=self.next_page)
        self.next_button.pack(side=tk.LEFT, padx=5)

        self.page_label = tk.Label(self.page_control_frame, text="Страница 1 из 1")
        self.page_label.pack(side=tk.LEFT, padx=5)

        tk.Label(self.page_control_frame, text="Перейти к странице:").pack(side=tk.LEFT, padx=5)
        self.page_entry = ttk.Entry(self.page_control_frame, width=5)
        self.page_entry.pack(side=tk.LEFT, padx=5)
        self.page_go_button = tk.Button(self.page_control_frame, text="Перейти", command=self.goto_page)
        self.page_go_button.pack(side=tk.LEFT, padx=5)

    def update_tree(self, products, page=1, items_per_page=10):
        self.tree.delete(*self.tree.get_children())  # Очистка дерева перед добавлением новых данных
        start_index = (page - 1) * items_per_page
        end_index = start_index + items_per_page
        for product in products[start_index:end_index]:
            self.tree.insert('', 'end', values=(product['product_name'], product['manufacturer_name'], product['manufacturer_id'], product['quantity'], product['warehouse_address']))

        self.update_page_label(page, len(products), items_per_page)

    def update_page_label(self, current_page, total_items, items_per_page):
        total_pages = (total_items + items_per_page - 1) // items_per_page
        self.page_label.config(text=f"Страница {current_page} из {total_pages}")
        self.prev_button.config(state=tk.NORMAL if current_page > 1 else tk.DISABLED)
        self.next_button.config(state=tk.NORMAL if current_page < total_pages else tk.DISABLED)

    def prev_page(self):
        current_page = int(self.page_label.cget("text").split()[1])
        if current_page > 1:
            self.controller.show_page(current_page - 1)

    def next_page(self):
        current_page = int(self.page_label.cget("text").split()[1])
        total_pages = int(self.page_label.cget("text").split()[-1])
        if current_page < total_pages:
            self.controller.show_page(current_page + 1)

    def goto_page(self):
        try:
            page = int(self.page_entry.get())
            total_pages = int(self.page_label.cget("text").split()[-1])
            if 1 <= page <= total_pages:
                self.controller.show_page(page)
            else:
                messagebox.showinfo("Ошибка", f"Введите страницу от 1 до {total_pages}")
        except ValueError:
            messagebox.showinfo("Ошибка", "Введите допустимое значение страницы")

    def set_controller(self, controller):
        self.controller = controller

class AddProductDialog(simpledialog.Dialog):
    def body(self, master):
        self.title("Добавить продукт")

        tk.Label(master, text="Название товара:").grid(row=0)
        self.product_name = tk.Entry(master)
        self.product_name.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(master, text="Название производителя:").grid(row=1)
        self.manufacturer_name = tk.Entry(master)
        self.manufacturer_name.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(master, text="УНП производителя:").grid(row=2)
        self.manufacturer_id = tk.Entry(master)
        self.manufacturer_id.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(master, text="Количество:").grid(row=3)
        self.quantity = tk.Entry(master)
        self.quantity.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(master, text="Адрес склада:").grid(row=4)
        self.warehouse_address = tk.Entry(master)
        self.warehouse_address.grid(row=4, column=1, padx=5, pady=5)

        return self.product_name  # initial focus

    def apply(self):
        self.result = {
            'product_name': self.product_name.get(),
            'manufacturer_name': self.manufacturer_name.get(),
            'manufacturer_id': self.manufacturer_id.get(),
            'quantity': self.quantity.get(),
            'warehouse_address': self.warehouse_address.get()
        }
