import tkinter
from view.abstract.subwindow import Subwindow
from view.main_window import MainWindow


class NewBookWindow(Subwindow):

    window_title = "Book Creation"

    events = "<ok_button_click>",

    enter_pack_kwargs = {
        "fill": tkinter.BOTH,
        "expand": True,
        "side": tkinter.RIGHT,
        "padx": 10,
        "pady": 10,
        "ipadx": 3,
        "ipady": 3,
    }

    label_pack_kwargs = {
        "fill": tkinter.BOTH,
        "side": tkinter.LEFT,
        "expand": False,
        "padx": 10,
        "pady": 10,
        "ipadx": 3,
        "ipady": 3,
    }

    button_pack_kwargs = {
        "fill": tkinter.X,
        "expand": False,
        "side": tkinter.LEFT,
        "padx": 10,
        "pady": 10,
        "ipadx": 3,
        "ipady": 3,
    }

    frame_pack_args = {
        "fill": tkinter.BOTH,
    }

    book_creating_args = (
        "title",
        "author_fio",
        "publisher",
        "volumes_num",
        "circulation"
    )

    def _build(self) -> None:
        self.args_vars = {arg: tkinter.StringVar(self) for arg in self.book_creating_args}
        for arg, var in self.args_vars.items():
            frame = tkinter.Frame(self)
            label = tkinter.Label(frame, text=f"{arg.capitalize()}:")
            label.pack(**self.label_pack_kwargs)
            entry = tkinter.Entry(frame, textvariable=var)
            entry.pack(**self.enter_pack_kwargs)
            frame.pack(**self.frame_pack_args)
        frame = tkinter.Frame(self)
        self.ok_button = tkinter.Button(frame, text="Ok", command=self.__click)
        self.ok_button.pack(**self.button_pack_kwargs)
        self.cancel_button = tkinter.Button(frame, text="Cancel", command=lambda: self.destroy())
        self.cancel_button.pack(**self.button_pack_kwargs)
        frame.pack(**self.frame_pack_args)

    def __click(self):
        kwargs = {arg: var.get() for arg, var in self.args_vars.items()}
        self._notify(
            "<ok_button_click>",
            **kwargs
        )


if __name__ == "__main__":
    window = NewBookWindow(None)
    window.mainloop()