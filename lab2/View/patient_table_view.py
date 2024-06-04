import tkinter as tk
from tkinter import ttk

class PatientTableView:
    def __init__(self, window, controller):
        self.controller = controller

        self.labels = ["ФИО пациента", "Адрес прописки", "Дата рождения", "Дата приема", "ФИО врача", "Заключение"]
        self.tree = ttk.Treeview(window, columns=self.labels, show='headings', style='Custom.Treeview')

        style = ttk.Style()
        style.configure('Custom.Treeview', font=('Arial', 12))
        style.configure('Custom.Treeview.Heading', font=('Arial', 14, 'bold'))

        for label in self.labels:
            self.tree.heading(label, text=label)

        self.tree.grid(row=0, column=2, rowspan=len(self.labels) + 1, padx=20, pady=10)

        self.page_label = tk.Label(window, text="", font=('Arial', 14))
        self.page_label.grid(row=len(self.labels) + 2, column=2, pady=10)

        self.nav_frame = tk.Frame(window)
        self.nav_frame.grid(row=len(self.labels) + 3, column=2, columnspan=4, pady=10)

        first_button = tk.Button(self.nav_frame, text="<<", command=lambda: self.navigate_page(1), font=('Arial', 12))
        first_button.grid(row=0, column=0, padx=5)

        previous_button = tk.Button(self.nav_frame, text="<", command=lambda: self.navigate_page(self.controller.current_page - 1), font=('Arial', 12))
        previous_button.grid(row=0, column=1, padx=5)

        next_button = tk.Button(self.nav_frame, text=">", command=lambda: self.navigate_page(self.controller.current_page + 1), font=('Arial', 12))
        next_button.grid(row=0, column=2, padx=5)

        last_button = tk.Button(self.nav_frame, text=">>", command=lambda: self.navigate_page(self.controller.total_pages), font=('Arial', 12))
        last_button.grid(row=0, column=3, padx=5)

    def navigate_page(self, page):
        if 1 <= page <= self.controller.total_pages:
            self.controller.current_page = page
            self.update_table()

    def update_table(self, patients=None):
        self.tree.delete(*self.tree.get_children())
        if patients is None:
            patients = self.controller.get_patients_for_page()

        for patient in patients:
            self.tree.insert('', 'end', values=[
                patient.full_name,
                patient.address,
                patient.birth_date,
                patient.appointment_date,
                patient.doctor_name,
                patient.conclusion
            ])

        self.page_label.config(text=f"Страница {self.controller.current_page}/{self.controller.total_pages}")
