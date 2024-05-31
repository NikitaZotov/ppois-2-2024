import tkinter
import utils as utils
from view.abstract.window import Window


class MainWindow(Window):

    window_title = "Books Main Menu"

    events = (
        # xml
        "<xml_save_menu_click>",
        "<xml_load_menu_click>",
        # database
        "<commit_button_click>",
        # records
        "<add_book_menu_click>",
        "<search_book_menu_click>",
        "<delete_book_menu_click>",
        # buttons
        "<first_page_button_click>",
        "<last_page_button_click>",
        "<prev_page_button_click>",
        "<next_page_button_click>",
        "<inc_pages_button_click>",
        "<dec_pages_button_click>",
        # checkbutton
        "<tree_view_checkbutton_click>"
    )

    books_tree_columns = {
        "title": "Title",
        "author_fio": "Author",
        "publisher": "Publisher",
        "volumes_num": "Volumes",
        "circulation": "Circulation",
        "total_volumes": "Total Volumes"
    }

    frame_pack_args = {
        "fill": tkinter.BOTH,
        "side": tkinter.TOP,
    }

    tree_pack_args = {
        "fill": tkinter.BOTH,
        "side": tkinter.LEFT,
        "expand": True,
        "padx": 10,
        "pady": 10,
    }

    button_pack_args = {
        "fill": tkinter.X,
        "side": tkinter.LEFT,
        "expand": True,
        "padx": 10,
        "pady": 10,
        "ipadx": 2,
        "ipady": 2,
    }

    indexes = {
        "page size",
        "total records",
        "current page",
        "total pages",
    }

    def _build(self) -> None:
        # xml-menu
        xml_menu = tkinter.Menu(tearoff=0)
        xml_menu.add_command(
            label="Save to xml",
            command=lambda: self._notify("<xml_save_menu_click>")
        )
        xml_menu.add_command(
            label="Load from xml",
            command=lambda: self._notify("<xml_load_menu_click>")
        )
        # record-menu
        record_menu = tkinter.Menu(tearoff=0)
        record_menu.add_command(
            label="Add book",
            command=lambda: self._notify("<add_book_menu_click>")
        )
        record_menu.add_command(
            label="Search books",
            command=lambda: self._notify("<search_book_menu_click>")
        )
        record_menu.add_command(
            label="Delete books",
            command=lambda: self._notify("<delete_book_menu_click>")
        )
        # main-menu
        main_menu = tkinter.Menu(tearoff=0)
        main_menu.add_cascade(
            label="Xml",
            menu=xml_menu
        )
        main_menu.add_cascade(
            label="Books",
            menu=record_menu
        )
        # window config
        self.config(menu=main_menu)
        tree_frame = tkinter.Frame()
        tree_frame.pack(**self.frame_pack_args, expand=True)
        self.book_tree = utils.build_tree(
            self.books_tree_columns,
            tree_frame,
            self.tree_pack_args
        )
        # buttons
        button_frame = tkinter.Frame()
        button_frame.pack(**self.frame_pack_args)
        button_frame = tkinter.Frame()
        button_frame.pack(**self.frame_pack_args)
        # button to go to the first page
        first_button = tkinter.Button(
            button_frame,
            text="First",
            underline=0,
            command=lambda: self._notify("<first_page_button_click>")
        )
        first_button.pack(**self.button_pack_args)
        # button to go to the previous page
        prev_button = tkinter.Button(
            button_frame,
            text="Previous",
            underline=0,
            command=lambda: self._notify("<prev_page_button_click>")
        )
        prev_button.pack(**self.button_pack_args)
        # decrease page size button
        dec_button = tkinter.Button(
            button_frame,
            text='-',
            command=lambda: self._notify("<dec_pages_button_click>")
        )
        dec_button.pack(**self.button_pack_args)
        # indexes start
        indexes_frame = tkinter.Frame(button_frame)
        # commit button
        commit_button = tkinter.Button(
            indexes_frame,
            text='Database Commit',
            command=lambda: self._notify("<commit_button_click>")
        )
        commit_button.pack()
        # indexes
        self.indexes = {index: tkinter.IntVar() for index in self.indexes}
        for index, var in self.indexes.items():
            frame = tkinter.Frame(indexes_frame)
            label = tkinter.Label(
                frame,
                text=f"{index.capitalize()}: ",
            )
            label.pack(side=tkinter.LEFT)

            index_label = tkinter.Label(
                frame,
                textvariable=var,
            )
            index_label.pack(side=tkinter.LEFT)
            frame.pack()
        # tree view button
        self.tree_view_enabled = tkinter.BooleanVar(indexes_frame)
        tree_view_checkbutton = tkinter.Checkbutton(
            variable=self.tree_view_enabled,
            text="Tree view",
            command=lambda: self._notify("<tree_view_checkbutton_click>")
        )
        tree_view_checkbutton.pack()
        indexes_frame.pack(**self.button_pack_args)
        # indexes end
        # increase page size button
        inc_button = tkinter.Button(
            button_frame,
            text='+',
            command=lambda: self._notify("<inc_pages_button_click>")
        )
        inc_button.pack(**self.button_pack_args)
        # button to go to the next page
        next_button = tkinter.Button(
            button_frame,
            text="Next",
            underline=0,
            command=lambda: self._notify("<next_page_button_click>")
        )
        next_button.pack(**self.button_pack_args)
        # button to go to the last page
        last_button = tkinter.Button(
            button_frame,
            text="Last",
            underline=0,
            command=lambda: self._notify("<last_page_button_click>")
        )
        last_button.pack(**self.button_pack_args)


if __name__ == "__main__":
    MainWindow().mainloop()
