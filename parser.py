from scanner import Scanner
from utils import write_parse_tree_to_file, write_syntax_errors_to_file
from parse_tree import get_parse_tree


class Parser:
    def __init__(self, scanner: Scanner):
        self.scanner = scanner
        self.curret_token = ""
        self.parse_tree = get_parse_tree()
        self.nodes_buffer = []
        self.syntax_errors = []

    def get_next_token(self):
        token = self.scanner.get_next_token()
        self.curret_token = token

    def save_to_file(self):
        write_syntax_errors_to_file(self.syntax_errors)
        write_parse_tree_to_file(self.parse_tree)

    def start(self):
        self.get_next_token()
        print("INIT")
