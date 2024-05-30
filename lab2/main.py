import tkinter as tk
from Controller.main_controller import MainController
from View.interface import Interface
from Model.database import Database
# This is a sample Python script.




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    model = Database("Model/tournaments.xml")
    controller = MainController(model)
    gui = Interface(controller)
