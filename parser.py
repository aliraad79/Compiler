from typing import List, Tuple
from scanner import Scanner, Token
from utils import (
    write_parse_tree_to_file,
    write_syntax_errors_to_file,
    print_parser_log,
    reverse_format_non_terminal,
)
from parse_tree import get_transation_diagrams, DiagramNode, IllegalToken, MissingToken
from anytree import Node


class Parser:
    def __init__(self, scanner: Scanner):
        self.scanner = scanner

        self.transation_diagrams: dict[str, DiagramNode] = get_transation_diagrams()
        self.nodes_buffer: List[str] = []
        self.return_nodes: List[Tuple[DiagramNode, DiagramNode]] = []
        self.parse_tree_root = Node("Program")

        self.current_token: Token = None
        self.current_node: DiagramNode = self.transation_diagrams["program"]

        self.syntax_errors: List = []

    def get_next_token(self):
        self.current_token = self.scanner.get_next_token()

    def save_to_file(self):
        write_syntax_errors_to_file(self.syntax_errors)
        write_parse_tree_to_file(self.parse_tree_root)

    def log(self):
        print_parser_log(self.current_node, self.current_token, self.return_nodes)

    def start(self):
        self.get_next_token()
        current_parse_node = self.parse_tree_root
        terminal = False
        while True:
            if self.current_node:
                try:
                    (
                        self.current_node,
                        terminal,
                        next_parse_node_name,
                    ) = self.current_node.next_diagram_tree_node(
                        self.current_token,
                        self.nodes_buffer,
                        reverse_format_non_terminal(current_parse_node.name),
                    )
                except IllegalToken:
                    self.syntax_errors.append(
                        f"#{self.scanner.line_number + 1} : syntax error, illegal {self.current_token.lexeme if self.current_token.type != 'ID' else self.current_token.type}"
                    )
                    self.get_next_token()
                    continue
                except MissingToken:
                    self.syntax_errors.append(
                        f"#{self.scanner.line_number + 1} : syntax error, missing {current_parse_node.name}"
                    )
                    self.current_node = self.transation_diagrams[
                        self.nodes_buffer.pop(len(self.nodes_buffer) - 1)
                    ]
                    continue

                if next_parse_node_name:
                    current_parse_node = Node(
                        next_parse_node_name if not terminal else self.current_token,
                        current_parse_node,
                    )
                else:
                    current_parse_node = current_parse_node.parent

                if not self.current_node:
                    current_parse_node = current_parse_node.parent

                if len(self.nodes_buffer) != 0:
                    if len(self.current_node.next_edges) != 0:
                        self.return_nodes.append(
                            (self.current_node, current_parse_node)
                        )

                    self.current_node = self.transation_diagrams[
                        self.nodes_buffer.pop(len(self.nodes_buffer) - 1)
                    ]

                if terminal:
                    current_parse_node = current_parse_node.parent
                    self.get_next_token()
                    terminal = False
            else:
                self.current_node, current_parse_node = self.return_nodes.pop(
                    len(self.return_nodes) - 1
                )
                current_parse_node = current_parse_node.parent

            if self.current_token.lexeme == "$" and len(self.return_nodes) == 0:
                Node("$", self.parse_tree_root)
                break
