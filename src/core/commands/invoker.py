from src.core.commands.abstract import ICommand


class CommandInvoker:

    def __init__(self):
        self.history = []

    def execute_command(self, command: ICommand):
        self.history.append(command)
        return command.execute()
