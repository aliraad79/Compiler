from scanner import Scanner
from utils import write_parse_tree_to_file, write_syntax_errors_to_file


class Parser:
    def __init__(self, scanner: Scanner):
        self.scanner = scanner
        self.curret_token = ""
        self.parse_tree = ...
        self.syntax_errors = []

    def get_next_token(self):
        self.curret_token = self.scanner.get_next_token()

    def save_to_file(self):
        write_syntax_errors_to_file(self.syntax_errors)
        write_parse_tree_to_file(self.parse_tree)

    def start(self):
        print("INIT")
