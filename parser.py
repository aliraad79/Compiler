from typing import List, Tuple
from icg import IntermidateCodeGenerator
from scanner import Scanner, Token
from utils import (
    write_parse_tree_to_file,
    write_syntax_errors_to_file,
    print_parser_log,
    reverse_format_non_terminal,
)
from parse_diagram import (
    get_transation_diagrams,
    DiagramNode,
    IllegalToken,
    MissingToken,
)
from anytree import Node


class Parser:
    def __init__(self, scanner: Scanner, icg: IntermidateCodeGenerator):
        self.scanner = scanner

        self.transation_diagrams: dict[str, DiagramNode] = get_transation_diagrams()
        self.past_node_stack: List[Tuple[DiagramNode, DiagramNode]] = []
        self.parse_tree_root = Node("Program")

        self.current_token: Token = None
        self.current_node: DiagramNode = self.transation_diagrams["program"]

        self.syntax_errors: List = []
        self.parse_node: Node = self.parse_tree_root

        self.icg = icg

        self.get_next_token()

    def get_next_token(self):
        self.current_token = self.scanner.get_next_token()

    def save_to_file(self):
        write_syntax_errors_to_file(self.syntax_errors)
        write_parse_tree_to_file(self.parse_tree_root)

    def log(self):
        print_parser_log(self.current_node, self.current_token, self.past_node_stack)

    def add_syntax_error(self, message):
        self.syntax_errors.append(message)

    def start_parsing(self):
        found_terminal = False

        # TODO refactore this function
        while True:
            try:
                # walk through parse diagram
                (
                    self.current_node,
                    found_terminal,
                    next_parse_node_name,
                    return_node_name,
                    action_symbol,
                ) = self.current_node.next_diagram_tree_node(
                    self.current_token,
                    reverse_format_non_terminal(self.parse_node.name),
                )

                if action_symbol != None:
                    self.icg.code_gen(
                        action_symbol,
                        self.current_token.lexeme,
                        self.scanner.symbol_table,
                    )

            except IllegalToken:
                self.add_syntax_error(
                    f"#{self.scanner.line_number} : syntax error, {self.current_token.ilegal_token_message}"
                )
                if self.current_token.lexeme == "$":
                    # remove orphan nodes
                    self.parse_node.parent.children = [
                        i
                        for i in self.parse_node.parent.children
                        if i != self.parse_node
                    ]
                    break

                # get next token after illegal token happens
                self.get_next_token()
                continue

            except MissingToken as e:
                self.syntax_errors.append(
                    f"#{self.scanner.line_number} : syntax error, missing {e.next_edge.parse_tree_name}"
                )
                # walk forward in diagram
                self.current_node = e.next_edge.next_node
                continue

            # can walk in diagram tree
            if next_parse_node_name:
                self.parse_node = Node(
                    next_parse_node_name if not found_terminal else self.current_token,
                    self.parse_node,
                )
            # fall back to last diagram
            else:
                self.parse_node = self.parse_node.parent

            if not self.current_node:
                if not self.parse_node:
                    break
                self.parse_node = self.parse_node.parent

            # go deep to another diagram
            if return_node_name:
                if len(self.current_node.next_edges) != 0:
                    self.past_node_stack.append((self.current_node, self.parse_node))

                self.current_node = self.transation_diagrams[return_node_name]

            # terminal is matched
            if found_terminal:
                self.parse_node = self.parse_node.parent
                self.get_next_token()
                found_terminal = False

            # end of parse
            if self.current_token.lexeme == "$" and len(self.past_node_stack) == 0:
                break

            # move back current_node pointer to last return node
            if not self.current_node:
                self.current_node, self.parse_node = self.past_node_stack.pop(
                    len(self.past_node_stack) - 1
                )
                self.parse_node = self.parse_node.parent
