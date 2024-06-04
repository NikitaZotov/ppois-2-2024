import tkinter as tk
from tkinter import ttk
from controllers.sportsman_controller import *

def update_table(tree, page_label):
    tree.delete(*tree.get_children())
    sportsmen = get_sportsmen_for_page(current_page)
    for sportsman in sportsmen:
        tree.insert('', 'end', values=[
            sportsman.full_name,
            sportsman.team,
            sportsman.position,
            sportsman.titles,
            sportsman.sport_type,
            sportsman.rank
        ])
    page_label.config(text=f"{current_page}/{total_pages}")

def navigate_page(tree, page_label, page):
    total_pages = get_total_pages()
    if 1 <= page <= total_pages:
        sportsmen = get_sportsmen_for_page(page)
        update_table(tree, page_label)
        page_label.config(text=f"{current_page}/{total_pages}")
