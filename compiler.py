# Jafar Sadeghi 97
# Ali Ahmadi Kafeshani 97105703
# No prints please
from enum import Enum
from typing import List
from utils import print_pretty
from file import add_tokens_to_file, add_symbols_to_symbol_table
import re


class TokenType(Enum):
    COMMENT = "(\/\*(\*(?!\/)|[^*])*\*\/)|(\/\/.*/n)"  # or EOF
    ID = "^[A-Za-z][A-Za-z0-9]*"
    KEYWORD = "if|else|void|int|repeat|break|until|return"
    NUM = "^[0-9]+"
    SYMBOL = ";|:|,|\[|\]|\(|\)|{|}|\+|-|\*|=|<|=="
    WHITESPACE = "\x09|\x0A|\x0B|\x0C|\x20"


class LexicalError(Enum):
    NO_ERROR = "There is no lexical error."
    INVALID_INPUT = "Invalid input"
    UNCLOSED_COMMENT = "Unclosed comment"  # just print 7 first chars and ...
    UNMATCHED_COMMENT = "Unmatched comment"
    INVALID_NUMBER = "Invalid number"


class Node:
    def __init__(
        self,
        char,
        nexts: List["Node"] = [],
        is_start=False,
        is_end=False,
        is_universal=False,
        next_universal_nodes: List["Node"] = [],
    ):
        self.char = char
        self.nexts = nexts
        self.is_start = is_start
        self.is_end = is_end
        self.is_universal = is_universal
        self.next_universal_nodes = next_universal_nodes

    def is_equal(self, other):
        return True if self.is_universal else self.char == other

    def __repr__(self):
        return f"{print_pretty(self.char)} with {len(self.nexts) if self.nexts else 0} nexts"


class Token:
    def __init__(self, _type: TokenType, lexeme):
        self.type = _type
        self.lexeme = lexeme


def get_next_char():
    global char_pointer, buffer

    char_pointer += 1
    with open("input.txt", "r") as file:
        char = file.read(char_pointer)
    buffer.append(char[char_pointer - 1 :])
    return char[char_pointer - 1 :]


def add_token_to_array(token) -> None:
    _type = ""
    for regex in TokenType:
        if re.search(regex.value, token):
            _type = regex
    

    if _type not in ["",TokenType.WHITESPACE, TokenType.COMMENT]:
        token_dict.setdefault(line_number, []).append(Token(_type.name, token))
        if _type in [TokenType.ID, TokenType.KEYWORD]:
            symbol_list.update([token])


def get_token_from_buffer():
    global buffer

    length = len(buffer) - 1
    token = buffer[:length]
    buffer = [buffer[length]]
    return "".join(token)


# global vars
token_dict: dict[int : List[Token]] = {}
symbol_list: set[str] = set()
error_list: List[str] = []

buffer: List[str] = []
line_number: int = 0
char_pointer = 0


if __name__ == "__main__":
    from dfa_tree import create_dfa_tree

    dfa_tree = create_dfa_tree()
    next_selected_nodes = []
    while True:

        # Fill char and next char with buffer otherwise get them from input file
        if buffer == []:
            char = get_next_char()
            next_char = get_next_char()
        else:
            if len(buffer) > 1:
                char = buffer[-2]
                next_char = buffer[-1]
            else:
                char = buffer[-1]
                next_char = get_next_char()

        # end of file
        if char == "":
            break

        # dfa nodes that is in start position an can be continued
        if next_selected_nodes == []:
            selected_nodes = [node for node in dfa_tree if node.char == char]
        else:
            selected_nodes = next_selected_nodes
            next_selected_nodes = []
        # Algorithm

        # No way to go in dfa tree --> possible token in buffer
        if len(selected_nodes) == 0:
            add_token_to_array(get_token_from_buffer())

        # Check if next character possibly can be append to our current state
        can_be_continued = False
        is_reach_end_of_universal = False
        next_nodes = []
        not_universal_next_nodes = []
        for option in selected_nodes:
            for node in option.nexts:
                if node.is_equal(next_char):
                    next_nodes.append(node)
                    can_be_continued = True
                    for j in option.next_universal_nodes:
                        if j.char == next_char :
                            not_universal_next_nodes.append(j)
                            is_reach_end_of_universal = True

        if buffer == [] and not can_be_continued:
            error_list.append(LexicalError.INVALID_INPUT.value + str(line_number))
        if line_number == 18:
            print(f"------- {line_number} -------")
            print(
                f"Current char : {print_pretty(char)} Next char : {print_pretty(next_char)}"
            )
            print(f"Buffer = {buffer}")
            print(f"Can be continued {can_be_continued}")
            print(f"Is reach end of universal {is_reach_end_of_universal}")
            print(
                f"Selected Nodes = {selected_nodes}\n\t\tWith nexts = {selected_nodes[0].nexts if len(selected_nodes) >= 1 else None}"
            )
            print(f"End of universal condition = {not_universal_next_nodes}")
        if can_be_continued and not is_reach_end_of_universal:
            char = next_char
            next_char = get_next_char()
            next_selected_nodes = (
                next_nodes
                if not_universal_next_nodes == []
                else not_universal_next_nodes
            )
        else:
            add_token_to_array(get_token_from_buffer())

        # next line
        if char == "\n":
            line_number += 1

    add_tokens_to_file(line_number, token_dict)
    add_symbols_to_symbol_table(symbol_list)
