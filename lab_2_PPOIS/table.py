import tkinter as tk
from tkinter import ttk, END, BOTH


class Window(tk.Tk):
    def __init__(self, people):
        super().__init__()

        self.title("Новое окно")
        self.geometry("1200x400")

        # определяем данные для отображения
        self.people = people

        # определяем столбцы
        self.columns = ("name", "birth_date", "team", "town", "sost", "pos")

        self.tree = ttk.Treeview(self, columns=self.columns, show="headings")
        self.tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        self.tree.heading("name", text="ФИО игрока")
        self.tree.heading("birth_date", text="Дата рождения")
        self.tree.heading("team", text="Футбольная команда")
        self.tree.heading("town", text="Домашний город")
        self.tree.heading("sost", text="Состав")
        self.tree.heading("pos", text="Позиция")

        # настраиваем столбцы

        # добавляем данные
        for person in self.people:
            self.tree.insert("", END, values=person)

