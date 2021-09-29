# Jafar Sadeghi 97
# Ali Ahmadi Kafeshani 97105703
# No prints please
from enum import Enum
from typing import List
import string


class TokenType(Enum):
    COMMENT = "(\/\*.*\/\*|\/\/.*\n)"  # or EOF
    ID = "[A-Za-z][A-Za-z0-9]*"
    KEYWORD = "(if|else|void|int|repeat|break|untill|return)"
    NUM = "[0-9]+"
    SYMBOL = "(;|:|,|\[|\]|\(|\)|{|}+|-|\*|=|<|==)"
    WHITESPACE = "(\x09|\x0A|\x0B|\x0C|\x20)"


class LexicalError(Enum):
    NO_ERROR = "There is no lexical error."
    INVALID_INPUT = "Invalid input"
    UNCLOSED_COMMENT = "Unclosed comment"  # just print 7 first chars and ...
    UNMATCHED_COMMENT = "Unmatched comment"
    INVALID_NUMBER = "Invalid number"


class Node:
    def __init__(self, char, nexts: List["Node"], is_start=False, is_end=False):
        self.char = char
        self.nexts = nexts
        self.is_start = is_start
        self.is_end = is_end
    
    def __repr__(self):
        return self.char


DFA_TREE: List[Node] = []


def create_dfa_tree():
    symbols = [";", ":", ",", "[", "]", "(", ")", "{", "}", "+", "-", "*", "=", "<"]
    symbol_tree = []
    for i in symbols:
        symbol_tree.append(Node(i, None, is_start=True, is_end=True))
    symbol_tree.append(Node("=", [Node("=", None, is_end=True)], is_start=True))
    whitespace_tree = []
    white = ["\x09", "\x0A", "\x0B", "\x0C", "\x20"]
    for i in white:
        whitespace_tree.append(Node(i, None, is_start=True, is_end=True))

    for i in range(10):
        exec(
            f'node_{i} = Node("{i}", None, is_start=True, is_end=True)',
            locals(),
            globals(),
        )
    # fmt: off
    node_0.nexts = [node_1,node_2,node_3,node_4,node_5,node_6,node_7,node_8,node_9]
    node_1.nexts = [node_0,node_2,node_3,node_4,node_5,node_6,node_7,node_8,node_9]
    node_2.nexts = [node_0,node_1,node_3,node_4,node_5,node_6,node_7,node_8,node_9]
    node_3.nexts = [node_0,node_1,node_2,node_4,node_5,node_6,node_7,node_8,node_9]
    node_4.nexts = [node_0,node_1,node_2,node_3,node_5,node_6,node_7,node_8,node_9]
    node_5.nexts = [node_0,node_1,node_2,node_3,node_4,node_6,node_7,node_8,node_9]
    node_6.nexts = [node_0,node_1,node_2,node_3,node_4,node_5,node_7,node_8,node_9]
    node_7.nexts = [node_0,node_1,node_2,node_3,node_4,node_5,node_6,node_8,node_9]
    node_8.nexts = [node_0,node_1,node_2,node_3,node_4,node_5,node_6,node_7,node_9]
    node_9.nexts = [node_0,node_1,node_2,node_3,node_4,node_5,node_6,node_7,node_8]
    number_tree =  [node_0,node_1,node_2,node_3,node_4,node_5,node_6,node_7,node_8,node_9]
    # fmt: on
    keyword_tree = []
    # if
    No_f = Node("f", None, is_end=True)
    No_i = Node("i", [No_f], is_start=True)
    keyword_tree.append(No_i)

    # int
    No_t = Node("t", None, is_end=True)
    No_n = Node("n", [No_t])
    No_i = Node("i", [No_n], is_start=True)
    keyword_tree.append(No_i)

    # else
    No_e = Node("e", None, is_end=True)
    No_s = Node("s", [No_e])
    No_l = Node("l", [No_s])
    No_e = Node("e", [No_l], is_start=True)
    keyword_tree.append(No_e)

    # void
    No_d = Node("d", None, is_end=True)
    No_i = Node("i", [No_d])
    No_o = Node("o", [No_i])
    No_v = Node("v", [No_o], is_start=True)
    keyword_tree.append(No_v)

    # repeat
    No_t = Node("t", None, is_end=True)
    No_a = Node("a", [No_t])
    No_e = Node("e", [No_a])
    No_p = Node("p", [No_e])
    No_e = Node("e", [No_p])
    No_r = Node("r", [No_e], is_start=True)
    keyword_tree.append(No_r)

    # break
    No_k = Node("k", None, is_end=True)
    No_a = Node("a", [No_k])
    No_e = Node("e", [No_a])
    No_r = Node("r", [No_e])
    No_b = Node("b", [No_r], is_start=True)
    keyword_tree.append(No_b)

    # untill
    No_l = Node("l", None, is_end=True)
    No_l = Node("l", [No_l])
    No_i = Node("i", [No_l])
    No_t = Node("t", [No_i])
    No_n = Node("n", [No_t])
    No_u = Node("u", [No_n], is_start=True)
    keyword_tree.append(No_u)

    # return
    No_n = Node("n", None, is_end=True)
    No_r = Node("r", [No_n])
    No_u = Node("u", [No_r])
    No_t = Node("t", [No_u])
    No_e = Node("e", [No_t])
    No_r = Node("r", [No_e], is_start=True)
    keyword_tree.append(No_r)

    id_tree = []

    for i in range(11):
        exec(f'node_{i} = Node("{i}", None, is_end=True)', locals(), globals())
        exec(f"id_tree.append(node_{i})", locals(), globals())
    for alphabet in string.ascii_letters:
        exec(
            f'node_{alphabet} = Node("{alphabet}", None, is_start=True, is_end=True)',
            locals(),
            globals(),
        )
        exec(f"id_tree.append(node_{alphabet})", locals(), globals())

    for i in string.ascii_letters:
        exec(f"node_{i}.nexts = id_tree", locals(), globals())

    return [*symbol_tree, *whitespace_tree, *number_tree, *keyword_tree, *id_tree]


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
    dfa_tree = create_dfa_tree()
    while True:
        pointer += 1
        try:
            token = get_next_token()
            print_pretty(token)
            if token == "":
                break
        except IndexError:
            break
