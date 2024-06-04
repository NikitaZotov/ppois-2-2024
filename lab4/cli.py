from src.view.terminal import Terminal
from src.view.consoleInputer import ConsoleInputer
from src.DAO.fileRepository import FileRepository
from src.controller.interpreter import Interpreter
from commands import commands


terminal = Terminal(
    ConsoleInputer(),
    Interpreter(commands),
    FileRepository(input("Enter name of file: "))
)

while True:
    try:
        print(terminal.do_iteration())
    except Exception as e:
        print(e)
