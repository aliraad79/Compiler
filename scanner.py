from __future__ import annotations
import re

from enum import Enum
from typing import List, Tuple

from dfa_tree import create_dfa_tree, State
from utils import *


class ErrorFound(Exception):
    pass


class TokenType(Enum):
    COMMENT = "(\/\*(\*(?!\/)|[^*])*\*\/)|(\/\/.*\n)"
    ID = "^[A-Za-z][A-Za-z0-9]*$"
    KEYWORD = "^(if|endif|else|void|int|repeat|break|until|return)$"
    NUM = "^[0-9]+$"
    SYMBOL = "^(;|:|,|\[|\]|\(|\)|{|}|\+|-|\*|=|<|==)$"
    WHITESPACE = "^(\x09|\x0A|\x0B|\x0C|\x20)$"


class LexicalError(Enum):
    UNMATCHED_COMMENT = ("\*/", "Unmatched comment")
    INVALID_NUMBER = ("^[0-9]+[^0-9]+$", "Invalid number")


class Token:
    def __init__(self, _type: TokenType, lexeme: str):
        self.type = _type
        self.lexeme = lexeme

    def __str__(self):
        return f"({self.type}, {self.lexeme})"


# global vars
token_dict: dict[int : List[Token]] = {}
symbol_list: list[str] = []
error_dict: dict[int:Tuple] = {}


class Scanner:
    def __init__(self):
        self.dfa_mother_state = create_dfa_tree()
        self.buffer = []
        self.line_number = 0
        self.char_pointer = 0
        self.char = ""
        self.next_char = ""
        self.last_comment_line_number = 0
        self.next_selected_state = None

    def get_next_token(self):
        # Fill char and next char with buffer otherwise get them from input file
        if self.buffer == []:
            self.char = self.get_next_char()
            self.next_char = self.get_next_char()
        else:
            if len(self.buffer) >= 2:
                self.char = self.buffer[-2]
                self.next_char = self.buffer[-1]
            else:
                self.char = self.buffer[-1]
                self.next_char = self.get_next_char()

        # next line
        if self.char == "\n":
            self.line_number += 1

        # update last_comment_line_number
        if self.char == "/" and (self.next_char in ["/", "*"]):
            self.last_comment_line_number = self.line_number

        # dfa states that is in start position an can be continued
        if self.next_selected_state == None:
            selected_state: State = self.dfa_mother_state.next_dfa_tree_state(self.char)
        else:
            selected_state = self.next_selected_state
            self.next_selected_state = None

        # Algorithm

        # Check if next character possibly can be append to our current state
        if selected_state:
            next_state = selected_state.next_dfa_tree_state(self.next_char)

        try:
            can_be_continued = next_state != None
        except NameError:
            can_be_continued = False

        # end of file
        if self.char == "":
            return Token(None, "$")

        if can_be_continued:
            self.char = self.next_char
            self.next_char = self.get_next_char()
            self.next_selected_state = next_state
        elif self.buffer != []:
            self.next_selected_state = None
            token = self.add_token_to_array()
            if token != None:
                return token

        return self.get_next_token()

    def get_next_char(self):
        self.char_pointer += 1
        with open("input.txt", "r") as file:
            char = file.read(self.char_pointer)
        self.buffer.append(char[self.char_pointer - 1 :])
        return char[self.char_pointer - 1 :]

    def add_token_to_array(self) -> None:
        token = self.get_token_from_buffer()

        try:
            _type = self.get_type_or_error(token)
        except ErrorFound:
            return None

        if _type not in ["", TokenType.WHITESPACE, TokenType.COMMENT]:
            token_dict.setdefault(self.line_number, []).append(Token(_type.name, token))
            if _type in [TokenType.ID, TokenType.KEYWORD]:
                if token not in symbol_list:
                    symbol_list.append(token)

        if _type not in ["", TokenType.WHITESPACE, TokenType.COMMENT]:
            return Token(_type.name, token)

    def get_token_from_buffer(self):
        length = len(self.buffer) - 1
        token = self.buffer[:length]
        self.buffer = [self.buffer[length]]
        return "".join(token)

    def save_to_file(self):
        add_tokens_to_file(self.line_number, token_dict)
        add_symbols_to_file(symbol_list)
        add_errors_to_file(self.line_number, error_dict)

    def get_type_or_error(self, token):
        if token == "":
            raise ErrorFound

        if token[:2] == "/*" and token[-2:] != "*/":
            error_dict.setdefault(self.last_comment_line_number, []).append(
                ("Unclosed comment", token[:7] + "..." if len(token) > 7 else "")
            )
            raise ErrorFound

        for error_regex in LexicalError:
            if re.match(error_regex.value[0], token):
                error_dict.setdefault(self.line_number, []).append(
                    (error_regex.value[1], token)
                )
                raise ErrorFound

        _type = ""
        for regex in TokenType:
            if re.search(regex.value, token):
                _type = regex

        if _type == "":
            error_dict.setdefault(self.line_number, []).append(("Invalid input", token))
            raise ErrorFound

        return _type
