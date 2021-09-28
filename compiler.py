# Jafar Sadeghi 97
# Ali Ahmadi Kafeshani 97105703
# No prints please
from enum import Enum


class TokenType(Enum):
    NUM = "[0-9]+"
    ID = "[A-Za-z][A-Za-z0-9]*"
    KEYWORD = "(if|else|void|int|repeat|break|untill|return)"
    SYMBOL = "(;|:|,|\[|\]|\(|\)|{|}+|-|\*|=|<|==)"
    COMMENT = "(\/\*.*\/\*|\/\/.*\n)"  # or EOF
    WHITESPACE = "(\x09|\x0A|\x0B|\x0C|\x20)"


class LexicalError(Enum):
    NO_ERROR = "There is no lexical error."
    INVALID_INPUT = "Invalid input"
    UNCLOSED_COMMENT = "Unclosed comment"  # just print 7 first chars and ...
    UNMATCHED_COMMENT = "Unmatched comment"
    INVALID_NUMBER = "Invalid number"


class Token:
    def __init__(self, _type: TokenType, lexeme):
        self.type = _type
        self.lexeme = lexeme


def get_next_token():
    with open("input.txt", "r") as file:
        char = file.read(pointer)

    return char[pointer - 1 :]


def add_token_to_file(token):
    with open("tokens.txt", "w") as file:
        pass


def add_error_to_file(string):
    with open("lexical_errors.txt", "w") as file:
        pass


def add_error_to_file(symbol: str):
    with open("symbol_table.txt", "w") as file:
        pass


def print_pretty(char):
    phrase = char
    if char == "\n":
        phrase = "\\n"
    elif char == "\t":
        phrase = "\\t"
    elif char == " ":
        phrase = "space"
    print(f" {phrase} ", end="")


lineno: int = 0
pointer: int = 0
if __name__ == "__main__":
    while True:
        pointer += 1
        try:
            token = get_next_token()
            print_pretty(token)
            if token == "":
                break
        except IndexError:
            break
