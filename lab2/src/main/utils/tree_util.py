import tkinter
import tkinter.ttk as ttk
from model.entity import Book


def add_book_to_tree(tree, book: Book):
    tree.insert(
        "",
        tkinter.END,
        iid=f"{book.title}",
        text=f"{book.title}",
        values=(
            book.title,
            book.author_fio,
            book.publisher,
            book.volumes_num,
            book.circulation,
            book.total_volumes,
        ),
    )
    for field, value in book:
        tree.insert(
            f"{book.title}",
            tkinter.END,
            text=value,
        )


def clear_tree(tree):
    for child in tree.get_children(""):
        tree.delete(child)


def build_tree(columns: dict[str, str], frame, pack_args, books: list[Book] | None = None) -> tkinter.ttk.Treeview:
    tree = tkinter.ttk.Treeview(
        frame,
        columns=list(columns),
        show="headings"
    )
    tree.column("#0", width=500)
    for column, head in columns.items():
        tree.heading(column, text=head)
    tree.pack(**pack_args)
    if books:
        for book in books:
            add_book_to_tree(tree, book)
    return tree