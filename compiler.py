# Jafar Sadeghi 97
# Ali Ahmadi Kafeshani 97105703
# No prints please

from __future__ import annotations
from enum import Enum
from typing import List, Tuple
import re
from utils import (
    print_log,
    add_tokens_to_file,
    add_symbols_to_file,
    add_errors_to_file,
)


class TokenType(Enum):
    COMMENT = "(\/\*(\*(?!\/)|[^*])*\*\/)|(\/\/.*/n)"  # or EOF
    ID = "^[A-Za-z][A-Za-z0-9]*"
    KEYWORD = "^(if|else|void|int|repeat|break|until|return)$"
    NUM = "^[0-9]+"
    SYMBOL = ";|:|,|\[|\]|\(|\)|{|}|\+|-|\*|=|<|=="
    WHITESPACE = "\x09|\x0A|\x0B|\x0C|\x20"


class LexicalError(Enum):
    # UNCLOSED_COMMENT = "Unclosed comment"
    # INVALID_INPUT = "Invalid input"
    UNMATCHED_COMMENT = ("\*/", "Unmatched comment")
    INVALID_NUMBER = ("^[0-9]+[A-Za-z]+", "Invalid number")


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
    if token == "":
        return None

    for error_regex in LexicalError:
        if re.match(error_regex.value[0], token):
            error_dict.setdefault(line_number, []).append((error_regex.value[1], token))
            break

    _type = ""
    for regex in TokenType:
        if re.search(regex.value, token):
            _type = regex

    if _type == "":
        error_dict.setdefault(line_number, []).append(("Invalid input", token))

    if _type not in ["", TokenType.WHITESPACE, TokenType.COMMENT]:
        token_dict.setdefault(line_number, []).append(Token(_type.name, token))
        if _type in [TokenType.ID, TokenType.KEYWORD]:
            if token not in symbol_list:
                symbol_list.append(token)


def get_token_from_buffer():
    global buffer

    length = len(buffer) - 1
    token = buffer[:length]
    buffer = [buffer[length]]
    return "".join(token)


def get_full_buffer():
    global buffer

    token = buffer
    buffer = []
    return "".join(token)


# global vars
token_dict: dict[int : List[Token]] = {}
symbol_list: list[str] = []
error_dict: dict[int:Tuple] = {}

buffer: List[str] = []
line_number: int = 0
char_pointer = 0

if __name__ == "__main__":
    from dfa_tree import create_dfa_tree, State

    dfa_mother_state_tree = create_dfa_tree()
    next_selected_state = None
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
            if buffer[0:2] == ["/", "*"]:
                comment = "".join(buffer)

                error_dict.setdefault(line_number, []).append(
                    (
                        "Unclosed comment",
                        "".join(comment if len(comment) <= 7 else comment[:7] + "..."),
                    )
                )
            break

        # dfa states that is in start position an can be continued
        if next_selected_state == None:
            selected_state: State = dfa_mother_state_tree.next_dfa_tree_state(char)
        else:
            selected_state = next_selected_state
            next_selected_state = None

        # Algorithm

        # Check if next character possibly can be append to our current state
        if selected_state:
            next_state = selected_state.next_dfa_tree_state(next_char)

        can_be_continued = next_state != None

        if line_number == 16 and True:
            print_log(
                buffer,
                char,
                next_char,
                selected_state,
                can_be_continued,
                line_number=18,
            )

        if can_be_continued:
            char = next_char
            next_char = get_next_char()
            next_selected_state = next_state
        elif buffer != []:
            add_token_to_array(get_token_from_buffer())
            next_selected_state = None

        # next line
        if char == "\n":
            line_number += 1

    add_tokens_to_file(line_number, token_dict)
    add_symbols_to_file(symbol_list)
    add_errors_to_file(line_number, error_dict)
