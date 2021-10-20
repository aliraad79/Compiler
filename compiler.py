# Jafar Sadeghi 97106079
# Ali Ahmadi Kafeshani 97105703

from __future__ import annotations
import re

from enum import Enum
from typing import List, Tuple

from dfa_tree import create_dfa_tree, State
from utils import *


class TokenType(Enum):
    COMMENT = "(\/\*(\*(?!\/)|[^*])*\*\/)|(\/\/.*\n)"
    ID = "^[A-Za-z][A-Za-z0-9]*$"
    KEYWORD = "^(if|else|void|int|repeat|break|until|return)$"
    NUM = "^[0-9]+$"
    SYMBOL = "^(;|:|,|\[|\]|\(|\)|{|}|\+|-|\*|=|<|==)$"
    WHITESPACE = "^(\x09|\x0A|\x0B|\x0C|\x20)$"


class LexicalError(Enum):
    UNMATCHED_COMMENT = ("\*/", "Unmatched comment")
    INVALID_NUMBER = ("^[0-9]+[^0-9]+$", "Invalid number")


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


def get_token_from_buffer():
    global buffer

    length = len(buffer) - 1
    token = buffer[:length]
    buffer = [buffer[length]]
    return "".join(token)


def add_token_to_array(token) -> None:
    global last_comment_line_number

    if token == "":
        return None

    if token[:2] == "/*" and token[-2:] != "*/":
        error_dict.setdefault(last_comment_line_number, []).append(
            ("Unclosed comment", token[:7] + "..." if len(token) > 7 else "")
        )
        return

    for error_regex in LexicalError:
        if re.match(error_regex.value[0], token):
            error_dict.setdefault(line_number, []).append((error_regex.value[1], token))
            return

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


# global vars
token_dict: dict[int : List[Token]] = {}
symbol_list: list[str] = []
error_dict: dict[int:Tuple] = {}

buffer = []
line_number: int = 0
char_pointer = 0
last_comment_line_number = 0

if __name__ == "__main__":

    dfa_mother_state_tree = create_dfa_tree()
    next_selected_state = None
    while True:

        # Fill char and next char with buffer otherwise get them from input file
        if buffer == []:
            char = get_next_char()
            next_char = get_next_char()
        else:
            if len(buffer) >= 2:
                char = buffer[-2]
                next_char = buffer[-1]
            else:
                char = buffer[-1]
                next_char = get_next_char()

        # next line
        if char == "\n":
            line_number += 1

        # update last_comment_line_number
        if char == "/" and (next_char in ["/", "*"]):
            last_comment_line_number = line_number

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

        try:
            can_be_continued = next_state != None
        except NameError:
            can_be_continued = False

        if line_number == 2 and False:
            print_log(
                buffer,
                char,
                next_char,
                selected_state,
                next_state,
                can_be_continued,
                line_number=line_number + 1,
            )

        # end of file
        if char == "":
            break

        if can_be_continued:
            char = next_char
            next_char = get_next_char()
            next_selected_state = next_state
        elif buffer != []:
            add_token_to_array(get_token_from_buffer())
            next_selected_state = None

    add_tokens_to_file(line_number, token_dict)
    add_symbols_to_file(symbol_list)
    add_errors_to_file(line_number, error_dict)
