from scanner import Scanner
from utils import write_parse_tree_to_file, write_syntax_errors_to_file
from parse_tree import get_parse_tree

class Parser:
    def __init__(self, scanner: Scanner):
        self.scanner = scanner
        self.curret_token = ""
        self.parse_tree = get_parse_tree()
        self.stack = []
        self.syntax_errors = []

    def get_next_token(self):
        self.curret_token = self.scanner.get_next_token()

    def save_to_file(self):
        write_syntax_errors_to_file(self.syntax_errors)
        write_parse_tree_to_file(self.parse_tree)

    def add_token_to_stack(self, token):
        self.stack.insert(0, token)

    def pop_stack_head(self):
        if len(self.stack) > 0:
            return self.stack.pop()
        # raise error maybe
        return None

    def start(self):
        print("INIT")
