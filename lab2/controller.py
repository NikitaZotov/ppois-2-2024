import tkinter as tk
import re
from tkinter import filedialog, ttk, messagebox
from model import Model
from view import View, AddProductDialog


class Controller:
    def __init__(self, root):
        self.model = Model()
        self.view = View(root)
        self.setup_callbacks()
        self.root = root
        self.refresh_button = None
        self.current_page = 1
        self.items_per_page = 10
        self.view.set_controller(self)

    def setup_callbacks(self):
        self.view.load_button.config(command=self.load_data)
        self.view.save_button.config(command=self.save_data)
        self.view.add_button.config(command=self.add_product)
        self.view.search_button.config(command=self.search_product)
        self.view.delete_button.config(command=self.delete_product)
        self.view.items_per_page_combobox.bind("<<ComboboxSelected>>", self.change_items_per_page)

    def add_product(self):
        pattern = re.compile(r'^-?\d+(\.\d+)?$')
        pattern2 = re.compile('^\d{3}\.\d{3}\.\d{3}$')
        dialog = AddProductDialog(self.view.root)
        if dialog.result:
            if not pattern.match(dialog.result.get("quantity")):
                messagebox.showinfo("Ошибка", "Количество должно быть числом")
                self.update_view()
                return
            if not pattern2.match(dialog.result.get("manufacturer_id")):
                messagebox.showinfo("Ошибка", "Неправильный формат упн")
                self.update_view()
                return
            if dialog.result.get("quantity") == '0':
                dialog.result["quantity"] = 'нет в наличии'
            self.model.add_product(dialog.result)
            self.update_view()

    def load_data(self):
        filename = filedialog.askopenfilename(title="Open XML File", filetypes=[("XML files", "*.xml")])
        if filename:
            self.model.load_from_file(filename)
            self.update_view()

    def save_data(self):
        filename = filedialog.asksaveasfilename(title="Save XML File", filetypes=[("XML files", "*.xml")],
                                                defaultextension=".xml")
        if filename:
            self.model.save_to_file(filename)

    def search_product(self):
        self.dialog1 = tk.Toplevel(self.root)
        self.dialog1.title("Поиск товара")

        screen_width = self.dialog1.winfo_screenwidth()
        screen_height = self.dialog1.winfo_screenheight()
        dialog_width = 300
        dialog_height = 500
        x = (screen_width // 2) - (dialog_width // 2)
        y = (screen_height // 2) - (dialog_height // 2)
        self.dialog1.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")

        self.criteria_vars = {}
        self.use_product_name_quantity = tk.BooleanVar()
        tk.Checkbutton(self.dialog1, text="Название товара или Количество на складе",
                       variable=self.use_product_name_quantity).pack(anchor=tk.W, pady=5)
        frame1 = tk.Frame(self.dialog1)
        frame1.pack(pady=5)
        self.criteria_vars["product_name_quantity"] = tk.StringVar(value="product_name")
        tk.Radiobutton(frame1, text="Название товара", variable=self.criteria_vars["product_name_quantity"],
                       value="product_name").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(frame1, text="Количество на складе", variable=self.criteria_vars["product_name_quantity"],
                       value="quantity").pack(side=tk.LEFT, padx=5)
        self.entry_product_name_quantity = ttk.Entry(self.dialog1)
        self.entry_product_name_quantity.pack(pady=5)

        self.use_manufacturer_name_id = tk.BooleanVar()
        tk.Checkbutton(self.dialog1, text="Название производителя или УНП производителя",
                       variable=self.use_manufacturer_name_id).pack(anchor=tk.W, pady=5)
        frame2 = tk.Frame(self.dialog1)
        frame2.pack(pady=5)
        self.criteria_vars["manufacturer_name_id"] = tk.StringVar(value="manufacturer_name")
        tk.Radiobutton(frame2, text="Название производителя", variable=self.criteria_vars["manufacturer_name_id"],
                       value="manufacturer_name").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(frame2, text="УНП", variable=self.criteria_vars["manufacturer_name_id"],
                       value="manufacturer_id").pack(side=tk.LEFT, padx=5)
        self.entry_manufacturer_name_id = ttk.Entry(self.dialog1)
        self.entry_manufacturer_name_id.pack(pady=5)

        self.use_warehouse_address = tk.BooleanVar()
        tk.Checkbutton(self.dialog1, text="Адрес склада", variable=self.use_warehouse_address).pack(anchor=tk.W, pady=5)
        self.entry_warehouse_address = ttk.Entry(self.dialog1)
        self.entry_warehouse_address.pack(pady=5)

        ok_button = tk.Button(self.dialog1, text="OK", command=lambda: self.execute_search(self.dialog1))
        ok_button.pack(pady=10)

        self.dialog1.wait_window()

    def execute_search(self, dialog):
        search_criteria = {}

        if self.use_product_name_quantity.get():
            selected_criterion = self.criteria_vars["product_name_quantity"].get()
            search_criteria[selected_criterion] = self.entry_product_name_quantity.get()

        if self.use_manufacturer_name_id.get():
            selected_criterion = self.criteria_vars["manufacturer_name_id"].get()
            search_criteria[selected_criterion] = self.entry_manufacturer_name_id.get()

        if self.use_warehouse_address.get():
            search_criteria["warehouse_address"] = self.entry_warehouse_address.get()

        results = self.model.search_product(search_criteria)
        if results:
            self.update_view(results)
            self.show_refresh_button()
        else:
            messagebox.showinfo("Search", "No matching products found.")
            self.update_view()
        dialog.destroy()

    def delete_product(self):
        self.dialog2 = tk.Toplevel(self.root)
        self.dialog2.title("Удаление товара")

        screen_width = self.dialog2.winfo_screenwidth()
        screen_height = self.dialog2.winfo_screenheight()
        dialog_width = 300
        dialog_height = 500
        x = (screen_width // 2) - (dialog_width // 2)
        y = (screen_height // 2) - (dialog_height // 2)
        self.dialog2.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")

        self.delete_criteria_vars = {}

        self.use_delete_product_name_quantity = tk.BooleanVar()
        tk.Checkbutton(self.dialog2, text="Название товара или Количество на складе",
                       variable=self.use_delete_product_name_quantity).pack(anchor=tk.W, pady=5)
        frame1 = tk.Frame(self.dialog2)
        frame1.pack(pady=5)
        self.delete_criteria_vars["product_name_quantity"] = tk.StringVar(value="product_name")
        tk.Radiobutton(frame1, text="Название товара", variable=self.delete_criteria_vars["product_name_quantity"],
                       value="product_name").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(frame1, text="Количество на складе", variable=self.delete_criteria_vars["product_name_quantity"],
                       value="quantity").pack(side=tk.LEFT, padx=5)
        self.entry_delete_product_name_quantity = ttk.Entry(self.dialog2)
        self.entry_delete_product_name_quantity.pack(pady=5)

        self.use_delete_manufacturer_name_id = tk.BooleanVar()
        tk.Checkbutton(self.dialog2, text="Название производителя или УНП производителя",
                       variable=self.use_delete_manufacturer_name_id).pack(anchor=tk.W, pady=5)
        frame2 = tk.Frame(self.dialog2)
        frame2.pack(pady=5)
        self.delete_criteria_vars["manufacturer_name_id"] = tk.StringVar(value="manufacturer_name")
        tk.Radiobutton(frame2, text="Название производителя",
                       variable=self.delete_criteria_vars["manufacturer_name_id"], value="manufacturer_name").pack(
            side=tk.LEFT, padx=5)
        tk.Radiobutton(frame2, text="УНП", variable=self.delete_criteria_vars["manufacturer_name_id"],
                       value="manufacturer_id").pack(side=tk.LEFT, padx=5)
        self.entry_delete_manufacturer_name_id = ttk.Entry(self.dialog2)
        self.entry_delete_manufacturer_name_id.pack(pady=5)

        self.use_delete_warehouse_address = tk.BooleanVar()
        tk.Checkbutton(self.dialog2, text="Адрес склада", variable=self.use_delete_warehouse_address).pack(anchor=tk.W,
                                                                                                           pady=5)
        self.entry_delete_warehouse_address = ttk.Entry(self.dialog2)
        self.entry_delete_warehouse_address.pack(pady=5)

        ok_button = tk.Button(self.dialog2, text="OK", command=lambda: self.execute_delete(self.dialog2))
        ok_button.pack(pady=10)

        self.dialog2.wait_window()

    def execute_delete(self, dialog):
        delete_criteria = {}

        if self.use_delete_product_name_quantity.get():
            selected_criterion = self.delete_criteria_vars["product_name_quantity"].get()
            delete_criteria[selected_criterion] = self.entry_delete_product_name_quantity.get()

        if self.use_delete_manufacturer_name_id.get():
            selected_criterion = self.delete_criteria_vars["manufacturer_name_id"].get()
            delete_criteria[selected_criterion] = self.entry_delete_manufacturer_name_id.get()

        if self.use_delete_warehouse_address.get():
            delete_criteria["warehouse_address"] = self.entry_delete_warehouse_address.get()

        self.model.delete_product(delete_criteria)
        self.update_view()
        dialog.destroy()

    def show_refresh_button(self):
        if not self.refresh_button:
            self.refresh_button = tk.Button(self.view.tool_frame, text="Обновить", command=self.refresh_data)
            self.refresh_button.pack(side=tk.LEFT, padx=5, pady=5)

    def refresh_data(self):
        self.update_view()
        self.refresh_button.pack_forget()
        self.refresh_button = None

    def update_view(self, data=None):
        if data is None:
            data = self.model.data
        self.current_page = 1
        self.view.update_tree(data, self.current_page, self.items_per_page)

    def show_page(self, page):
        self.current_page = page
        self.view.update_tree(self.model.data, self.current_page, self.items_per_page)

    def change_items_per_page(self, event):
        self.items_per_page = int(self.view.items_per_page_combobox.get())
        self.current_page = 1
        self.update_view()

    def goto_page(self):
        try:
            page = int(self.view.page_entry.get())
            total_pages = (len(self.model.data) + self.items_per_page - 1) // self.items_per_page
            if 1 <= page <= total_pages:
                self.show_page(page)
            else:
                messagebox.showinfo("Ошибка", f"Введите страницу от 1 до {total_pages}")
        except ValueError:
            messagebox.showinfo("Ошибка", "Введите допустимое значение страницы")


if __name__ == "__main__":
    root = tk.Tk()
    app = Controller(root)
    root.mainloop()
