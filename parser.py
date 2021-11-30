from typing import List
from scanner import Scanner, Token
from utils import (
    write_parse_tree_to_file,
    write_syntax_errors_to_file,
    print_parser_log,
)
from parse_tree import init_transation_diagrams, ParseTreeNode


class Parser:
    def __init__(self, scanner: Scanner):
        self.scanner = scanner
        self.curret_token: Token = None
        self.transation_diagrams: dict[str, ParseTreeNode] = init_transation_diagrams()
        self.current_node: ParseTreeNode = self.transation_diagrams["program"]
        self.parse_tree = None
        self.nodes_buffer: List = []
        self.return_nodes: List[ParseTreeNode] = []
        self.syntax_errors: List = []

    def get_next_token(self):
        self.curret_token = self.scanner.get_next_token()

    def save_to_file(self):
        write_syntax_errors_to_file(self.syntax_errors)
        write_parse_tree_to_file(self.parse_tree)

    def log(self):
        print_parser_log(self.nodes_buffer, self.current_node, self.curret_token)

    def start(self):
        print("INIT")
        self.get_next_token()
        terminal = False
        # while self.curret_token.lexeme != "$":
        for i in range(8):
            self.log()
            if self.current_node:
                self.current_node, terminal = self.current_node.next_parse_tree_node(
                    self.curret_token.lexeme
                )
                if len(self.nodes_buffer) != 0:
                    self.return_nodes.append(self.current_node)
                    self.current_node = self.transation_diagrams[
                        self.nodes_buffer.pop(0)
                    ]
                if terminal:
                    self.get_next_token()
            else:
                print(self.return_nodes)
                self.current_node = self.return_nodes.pop(0)
