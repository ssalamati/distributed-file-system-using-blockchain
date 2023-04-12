import sqlite3

from rich import print as rprint
from rich.console import Console
from rich.prompt import Prompt
from rich.tree import Tree

from file_handler import FileHandler

console = Console()


class ConsoleApp:
    def __init__(self, sdfs, db):
        self.db = db
        self.sdfs = sdfs

    def run(self):
        self.welcome()
        goodbye = False
        while not goodbye:
            choice = self.get_main_action()
            if choice == "1":
                self.upload_file()
            if choice == "2":
                self.download_file()
            if choice == "3":
                self.list_uploaded_files()
            if choice == "5":
                self.goodbye()
                goodbye = True

    @staticmethod
    def welcome():
        style1 = "blink bold yellow"
        console.rule(style="yellow")
        console.print("Welcome to the Super (or simple :D) Decentralized File System!", style=style1, justify="center")
        console.print("A server is up and running on your address, so that others can use your computer as an storage."
                      " Whenever you receive a new request, it will be handeled by SDFS and you will see the log, so"
                      " don't worry if you saw it in the middle of your work!", style=style1, justify="center")
        console.rule(style="yellow")

    @staticmethod
    def goodbye():
        style1 = "bold yellow"
        console.rule(style="yellow")
        console.print("Have a good day!", style=style1, justify="center")
        console.rule(style="yellow")

    @staticmethod
    def get_main_action():
        tree = Tree("\nWhat is your next step?")
        tree.add("1. Upload a new file")
        tree.add("2. Download a currently uploaded file")
        tree.add("3. List all uploaded files")
        tree.add("5. Exit")
        rprint(tree)
        choice = Prompt.ask(
            "Choose from",
            choices=["1", "2", "3", "5"],
        )
        return choice

    def upload_file(self):
        is_acceptable = False
        file_path = ""
        while not is_acceptable:
            file_path = Prompt.ask(
                "Please enter the address of the file",
            )
            try:
                open(file_path, 'rb')
            except FileNotFoundError:
                console.print("The file does not exist! Try again", style="bold red")
                continue
            is_acceptable = True
        file_handler = FileHandler(file_path)
        file_handler.split_file()
