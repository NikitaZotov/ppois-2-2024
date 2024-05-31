from presenter.main_presenter import MainPresenter
from view.main_window import MainWindow

window = MainWindow()
presenter = MainPresenter(window)
window.mainloop()