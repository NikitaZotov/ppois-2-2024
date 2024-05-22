import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox


class ClientView:
    def __init__(self, root):
        self.controller = None
        self.root = root

    def set_controller(self, controller):
        self.controller = controller

    def but_save(self):
        self.controller.save_clients_to_xml()
    def create_widgets(self):
        # Фрейм для таблицы
        self.tree_frame = tk.Frame(self.root)
        self.tree_frame.pack(pady=10)

        self.tree = ttk.Treeview(self.tree_frame, columns=('fio', 'account_number', 'address', 'mobile', 'phone'),
                                 show='headings')
        self.tree.heading('fio', text='ФИО')
        self.tree.heading('account_number', text='Номер счёта')
        self.tree.heading('address', text='Адрес')
        self.tree.heading('mobile', text='Мобильный номер')
        self.tree.heading('phone', text='Городской номер')
        self.tree.column('fio', minwidth=0, width=150)
        self.tree.column('account_number', minwidth=0, width=100)
        self.tree.column('address', minwidth=0, width=200)
        self.tree.column('mobile', minwidth=0, width=200)
        self.tree.column('phone', minwidth=0, width=200)
        self.tree.pack()

        # Фрейм для кнопок
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        # Кнопки для обработки данных клиентов
        self.add_button = tk.Button(self.button_frame, text='Добавить Клиента', command=self.open_add_client_dialog)
        self.find_button = tk.Button(self.button_frame, text='Найти Клиента', command=self.find_client_dialog)
        self.delete_button = tk.Button(self.button_frame, text='Удалить Клиента', command=self.delete_client_dialog)
        self.save_button = tk.Button(self.button_frame, text='Сохранить в файл', command= self.controller.save_clients_to_xml)
        self.load_button = tk.Button(self.button_frame, text='Загрузить из файла', command= self.controller.load_from_file)

        self.add_button.grid(row=0, column=0, padx=10)
        self.find_button.grid(row=0, column=1, padx=10)
        self.delete_button.grid(row=0, column=2, padx=10)
        self.save_button.grid(row=0, column=3, padx=10)
        self.load_button.grid(row=0, column=4, padx=10)

    def open_add_client_dialog(self):
        full_name = simpledialog.askstring("Добавление клиента", "Введите ФИО:", parent=self.root)

        account_number = simpledialog.askinteger("Добавление клиента", "Введите номер счета:", parent=self.root)

        address = simpledialog.askstring("Добавление клиента", "Введите адрес:", parent=self.root)

        mobile_phone = simpledialog.askinteger("Добавление клиента", "Введите мобильный номер телефона:",
                                              parent=self.root)

        landline_phone = simpledialog.askinteger("Добавление клиента", "Введите городской номер телефона:",
                                                parent=self.root)

        if all([full_name, account_number, address, mobile_phone, landline_phone]):
            client_info = {
                'full_name': str(full_name),
                'account_number': str(account_number),
                'address': str(address),
                'mobile_phone': str(mobile_phone),
                'landline_phone': str(landline_phone)
            }
            self.controller.add_client_to_model(client_info)  # Передаем данные в контроллер для добавления клиента
        else:
            tk.messagebox.showerror("Ошибка", "Все поля должны быть заполнены", parent=self.root)

    def find_client_dialog(self):
        search_query = simpledialog.askstring("Поиск клиента", "Введите условие поиска:")
        if search_query:
            search_params = self.parse_search_query(search_query)
            results = self.controller.find_client(search_params)
            if results:
                for client in results:
                    client_info = f"Имя: {client.get('full_name')}, Телефон: {client.get('mobile_phone')}, Адрес: {client.get('address')}\n"
                    messagebox.showinfo("Найден клиент", client_info)
            else:
                messagebox.showwarning("Результат поиска", "Клиент не найден.")

    def parse_search_query(self, query):
        query_parts = query.split(',')
        search_params = {}
        for part in query_parts:
            if part.isdigit():
                # Предполагаем, что это номер телефона или счета
                if len(part) == 6:  # условная длина номера счета
                    search_params['account_number'] = part
                else:
                    search_params['phone'] = part
            elif ' ' in part:
                # Предполагаем, что это ФИО
                search_params['full_name'] = part.strip()
            else:
                # Предполагаем, что это фамилия или адрес
                if part.isalpha():
                    search_params['surname'] = part.strip()
                    search_params['address'] = part.strip()
        return search_params

    def delete_client_dialog(self):
        query = simpledialog.askstring("Удаление клиента", "Введите данные для удаления клиента:")
        if query:
            self.controller.delete_client(query)

    def show_message(self, title, message):
        messagebox.showinfo(title, message)

    def create_pagination_controls(self):
        # Элементы управления для навигации по страницам
        self.pagination_frame = tk.Frame(self.root)
        self.pagination_frame.pack( fill=tk.X, padx = 300)

        self.first_page_button = tk.Button(self.pagination_frame, text="Первая страница", command=lambda: self.change_page('first'))
        self.first_page_button.pack(side=tk.LEFT)

        self.prev_page_button = tk.Button(self.pagination_frame, text="<", command=lambda: self.change_page('prev'))
        self.prev_page_button.pack(side=tk.LEFT)

        self.next_page_button = tk.Button(self.pagination_frame, text=">", command=lambda: self.change_page('next'))
        self.next_page_button.pack(side=tk.LEFT)

        self.last_page_button = tk.Button(self.pagination_frame, text="Последняя страница", command=lambda: self.change_page('last'))
        self.last_page_button.pack(side=tk.LEFT)

        # self.records_per_page_label = tk.Label(self.pagination_frame, text="0")
        # self.records_per_page_label.pack(side=tk.LEFT)

        self.total_records_label = tk.Label(self.pagination_frame, text="0")
        self.total_records_label.pack(side=tk.LEFT)

        self.current_page_label = tk.Label(self.pagination_frame, text="Страница 1")
        self.current_page_label.pack(side=tk.LEFT)

        self.total_pages_label = tk.Label(self.pagination_frame, text="из 1")
        self.total_pages_label.pack(side=tk.LEFT)

        self.label_records_per_page = tk.Label(self.pagination_frame, text='Записей на странице:')
        self.label_records_per_page.pack()

        self.combobox_records_per_page = ttk.Combobox(self.pagination_frame, values=[1, 5, 10, 25, 50], state="readonly")
        self.combobox_records_per_page.pack()
        self.combobox_records_per_page.bind('<<ComboboxSelected>>', self.on_records_per_page_changed)
        self.combobox_records_per_page.set(self.controller.get_records_per_page())

    def on_records_per_page_changed(self, event):
        new_value = int(self.combobox_records_per_page.get())
        self.controller.set_items_per_page(new_value)

    def update_view(self):
        # Очистка таблицы
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Заполнение таблицы новыми данными
        for client in self.controller.get_clients():
            self.tree.insert("", tk.END, values=(client["full_name"],
                                                 client["account_number"],
                                                 client["address"],
                                                 client["mobile_phone"],
                                                 client["landline_phone"]))

        self.update_pagination_info()

    def update_pagination_info(self):
        records_per_page = self.controller.get_records_per_page()
        total_records = self.controller.get_total_records()
        current_page = self.controller.get_current_page()
        total_pages = self.controller.get_total_pages()

        # self.records_per_page_label.config(text=f'{str(records_per_page)} клиентов на странице.')
        self.total_records_label.config(text=f"Всего записей: {total_records}")
        self.current_page_label.config(text=f"Страница {current_page}")
        self.total_pages_label.config(text=f"из {total_pages}")

    def change_page(self, action):
        if action == 'first':
            self.controller.first_page()
        elif action == 'prev':
            self.controller.previous_page()
        elif action == 'next':
            self.controller.next_page()
        elif action == 'last':
            self.controller.last_page()

        self.update_view()

    def on_records_per_page_changed(self, event):
        try:
            new_value = int(self.combobox_records_per_page.get())
            self.controller.set_items_per_page(new_value)
        except ValueError as e:
            self.show_message('Ошибка', 'Введите корректное число')
