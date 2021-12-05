from typing import List
from scanner import Scanner, Token
from utils import (
    write_parse_tree_to_file,
    write_syntax_errors_to_file,
    print_parser_log,
)
from parse_tree import init_transation_diagrams, DiagramNode
from anytree import Node, RenderTree


class Parser:
    def __init__(self, scanner: Scanner):
        self.scanner = scanner

        self.transation_diagrams: dict[str, DiagramNode] = init_transation_diagrams()
        self.parse_tree_repr: dict[int, str] = {}  # For test
        self.nodes_buffer: List[str] = []
        self.return_nodes: List[DiagramNode] = []

        self.current_token: Token = None
        self.current_node: DiagramNode = self.transation_diagrams["program"]

        self.syntax_errors: List = []

    def get_next_token(self):
        self.current_token = self.scanner.get_next_token()

    def save_to_file(self):
        write_syntax_errors_to_file(self.syntax_errors)
        write_parse_tree_to_file(self.parse_tree_repr)

    def log(self):
        print_parser_log(
            self.current_node, self.current_token, self.return_nodes, self.nodes_buffer
        )

    def start(self):
        parse_tree_root = Node("program")
        current_parse_node = parse_tree_root
        try:
            self.get_next_token()
            terminal = False
            while self.current_token.lexeme != "$":
                if self.current_node:
                    (
                        self.current_node,
                        terminal,
                    ) = self.current_node.next_parse_tree_node(
                        self.current_token,
                        self.nodes_buffer,
                        current_parse_node
                    )
                    if len(self.nodes_buffer) != 0:
                        if len(self.current_node.next_edges) != 0:
                            self.return_nodes.append(self.current_node)
                        self.current_node = self.transation_diagrams[
                            self.nodes_buffer.pop(len(self.nodes_buffer) - 1)
                        ]
                    if terminal:
                        Node(self.current_token, parent=current_parse_node)
                        self.get_next_token()
                        terminal = False
                else:
                    self.current_node = self.return_nodes.pop(
                        len(self.return_nodes) - 1
                    )
        except:
            # self.log()
            raise
        finally:
            Node("$", current_parse_node)
            print(RenderTree(parse_tree_root))
