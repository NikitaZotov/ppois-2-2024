import tkinter as tk
from tkinter import ttk

def create_labels_and_entries(window, labels):
    entries = []
    for i, label_text in enumerate(labels):
        label = tk.Label(window, text=label_text)
        label.grid(row=i, column=0, padx=10, pady=5)

        if label_text == "Состав":
            values1 = ["основной", "запасной", "n/a"]
            entry = ttk.Combobox(window, values=values1)
        elif label_text == "Разряд":
            values2 = ["1-й юношеский", "2-й разряд", "3-й разряд", "кмс", "мастер спорта"]
            entry = ttk.Combobox(window, values=values2)
        else:
            entry = tk.Entry(window)

        if label_text == "Титулы":
            entry.config(validate="key", validatecommand=(window.register(lambda char: char.isdigit() or char == ""), "%S"))

        entry.grid(row=i, column=1, padx=10, pady=5)
        entries.append(entry)
    return entries

def create_treeview(window, labels):
    tree = ttk.Treeview(window, columns=labels, show='headings')
    for label in labels:
        tree.heading(label, text=label)
    tree.grid(row=0, column=2, rowspan=len(labels) + 1, padx=10, pady=5)
    return tree
