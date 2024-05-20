from view import View
from model import Model
from controller import Controller

model = Model()
controller = Controller(model)
view = View(model, controller)
view.root.mainloop()
