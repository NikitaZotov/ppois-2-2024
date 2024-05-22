import tkinter as tk
from view import ClientView
from controller import ClientController
from model import ClientModel


def main():
    root = tk.Tk()
    root.title("Приложение для учета клиентов")
    root.geometry("1400x400+200+100")

    model = ClientModel()  # Создаем модель
    view = ClientView(root)  # Создаем вид
    controller = ClientController(view , model)  # Создаем контроллер с моделью
    view.set_controller(controller)  # Устанавливаем контроллер для вида

    root.mainloop()


if __name__ == "__main__":
    main()