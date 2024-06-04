from cli.computer_state_machine import ComputerStateMachine
from computer_parts.computer import Computer

state_machine = ComputerStateMachine(computer=Computer())
state_machine.run()
