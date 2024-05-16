import tkinter
from tkinter import ttk

import utils
from view.abstract.subwindow import Subwindow


class SearchBookWindow(Subwindow):
    window_title = "Book Search"

    events = (
        "<ok_button_click>",
        "<find_button_click>",
        "<higher_checkbutton_click>"
    )

    books_tree_columns = {
        "title": "Title",
        "author_fio": "Author",
        "publisher": "Publisher",
        "volumes_num": "Volumes",
        "circulation": "Circulation",
        "total_volumes": "Total Volumes"
    }

    label_pack_args = {
        "padx": 5,
        "pady": 5,
        "ipadx": 2,
        "ipady": 2,
    }

    entry_pack_args = {
        "padx": 5,
        "pady": 5,
        "ipadx": 2,
        "ipady": 2,
    }

    button_pack_args = {
        "side": tkinter.LEFT,
        "expand": True,
        "fill": tkinter.BOTH,
        "padx": 10,
        "pady": 10,
        "ipadx": 2,
        "ipady": 2,
    }

    tree_pack_args = {
        "padx": 10,
        "pady": 10,
    }

    frame_pack_args = {
    }

    notebook_pack_args = {
        "expand": True,
        "fill": tkinter.BOTH,
        "padx": 10,
        "pady": 10,
    }

    def _build(self) -> None:
        self.search_args: dict[str, tkinter.StringVar] = {}
        self.notebook = ttk.Notebook(self)
        self.notebook.add(
            self.__frame_for_searching_by("title"),
            text="Search by title"
        )
        self.notebook.add(
            self.__frame_for_searching_by("author_fio"),
            text="Search by author"
        )
        self.notebook.add(
            self.__frame_for_searching_by("author_fio", "publisher"),
            text="Search by author and publisher"
        )
        self.notebook.add(
            self.__frame_for_searching_by("volumes_from", "volumes_to"),
            text="Search by volumes number in range"
        )
        self.notebook.add(
            self.__frame_for_searching_by("circulation"),
            text="Search by circulation"
        )
        self.notebook.add(
            self.__frame_for_searching_by("total_volumes"),
            text="Search by total volumes"
        )
        self.notebook.pack(**self.notebook_pack_args)
        tree_frame = tkinter.Frame(self)
        self.search_tree = utils.build_tree(
            self.books_tree_columns,
            tree_frame,
            self.tree_pack_args
        )
        tree_frame.pack(**self.frame_pack_args)

        button_frame = tkinter.Frame(self)

        find_button = tkinter.Button(
            button_frame,
            text="Search",
            command=lambda: self._notify("<find_button_click>")
        )
        find_button.pack(**self.button_pack_args)

        ok_button = tkinter.Button(
            button_frame,
            text="Ok",
            command=lambda: self._notify("<ok_button_click>")
        )
        ok_button.pack(**self.button_pack_args)

        button_frame.pack(**self.frame_pack_args, fill=tkinter.X)

    def __frame_for_searching_by(self, *args) -> tkinter.Frame:
        entries_frame = tkinter.Frame(self)
        flag = False
        for arg in args:
            if arg == "circulation" or arg == "total_volumes":
                flag = True
            frame = tkinter.Frame(entries_frame)
            label = tkinter.Label(frame, text=arg.capitalize())
            label.pack(**self.label_pack_args)
            if arg in self.search_args:
                var = self.search_args[arg]
            else:
                var = tkinter.StringVar(self)
                self.search_args[arg] = var
            entry = tkinter.Entry(frame, textvariable=var)
            entry.pack(**self.entry_pack_args)
            if flag:
                higher_lower_checkbutton = tkinter.Checkbutton(
                    frame,
                    text="Higher (Default: Lower)",
                    command=lambda: self._notify("<higher_checkbutton_click>")
                )
                higher_lower_checkbutton.pack(**self.button_pack_args)
            frame.pack(
                **self.frame_pack_args,
                side=tkinter.LEFT,
                expand=True,
            )
        entries_frame.pack(**self.frame_pack_args, fill=tkinter.BOTH)
        return entries_frame


if __name__ == "__main__":
    window = SearchBookWindow(None)
    window.mainloop()
