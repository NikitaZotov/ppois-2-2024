from Model import *
from View import *
from Controller import *

if __name__ == "__main__":
    model = RecordModel()
    view = MainView()
    controller = Controller(model, view)
    view.set_controller(controller)
    view.mainloop()

