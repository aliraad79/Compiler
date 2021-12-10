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
            # self.log()
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
                if self.current_token.lexeme == "$":
                    self.syntax_errors.append(
                        f"#{self.scanner.line_number + 1} : syntax error, Unexpected EOF"
                    )
                    current_parse_node.parent.children = [
                        i
                        for i in current_parse_node.parent.children
                        if i != current_parse_node
                    ]
                    break
                self.syntax_errors.append(
                    f"#{self.scanner.line_number + 1} : syntax error, illegal {self.current_token.lexeme if self.current_token.type not in ['ID', 'NUM'] else self.current_token.type}"
                )
                self.get_next_token()
                next_parse_node_name = None
                continue

            except MissingToken as e:
                self.syntax_errors.append(
                    f"#{self.scanner.line_number + 1} : syntax error, missing {e.next_edge.get_node_name()}"
                )
                self.current_node = e.next_edge.next_node
                next_parse_node_name = None
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
                    self.return_nodes.append((self.current_node, current_parse_node))

                self.current_node = self.transation_diagrams[
                    self.nodes_buffer.pop(len(self.nodes_buffer) - 1)
                ]

            # terminal is matched
            if terminal:
                current_parse_node = current_parse_node.parent
                self.get_next_token()
                terminal = False

            # end of parse
            if self.current_token.lexeme == "$" and len(self.return_nodes) == 0:
                break

            # move back current_node pointer to last return node
            if not self.current_node:
                self.current_node, current_parse_node = self.return_nodes.pop(
                    len(self.return_nodes) - 1
                )
                current_parse_node = current_parse_node.parent
