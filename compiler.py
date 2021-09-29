# Jafar Sadeghi 97
# Ali Ahmadi Kafeshani 97105703
# No prints please
from enum import Enum
from typing import List
from utils import print_pretty
from file import add_tokens_to_file
import string
import re


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
    def __init__(self, char, nexts: List["Node"] = [], is_start=False, is_end=False):
        self.char = char
        self.nexts = nexts
        self.is_start = is_start
        self.is_end = is_end

    def __repr__(self):
        return f"{self.char} with {len(self.nexts) if self.nexts else 0} nexts"


class Token:
    def __init__(self, _type: TokenType, lexeme):
        self.type = _type
        self.lexeme = lexeme


def create_dfa_tree():

    # Create Symbol nodes
    symbol_tree = []
    for i in [";", ":", ",", "[", "]", "(", ")", "{", "}", "+", "-", "*", "=", "<"]:
        symbol_tree.append(Node(i, [], is_start=True, is_end=True))
    # Add == to symbol tree
    symbol_tree.append(Node("=", [Node("=", [], is_end=True)], is_start=True))

    # Create whitespace tree
    whitespace_tree = []
    white_spaces = ["\x09", "\x0A", "\x0B", "\x0C", "\x20"]
    for i in white_spaces:
        whitespace_tree.append(Node(i, [], is_start=True, is_end=True))

    # Create num tree
    for i in range(10):
        exec(
            f'node_{i} = Node("{i}", [], is_start=True, is_end=True)',
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

    # Create keyword tree
    keyword_tree = []
    # if
    No_f = Node("f", [], is_end=True)
    No_i = Node("i", [No_f], is_start=True)
    keyword_tree.append(No_i)

    # int
    No_t = Node("t", [], is_end=True)
    No_n = Node("n", [No_t])
    No_i = Node("i", [No_n], is_start=True)
    keyword_tree.append(No_i)

    # else
    No_e = Node("e", [], is_end=True)
    No_s = Node("s", [No_e])
    No_l = Node("l", [No_s])
    No_e_1 = Node("e", [No_l], is_start=True)
    keyword_tree.append(No_e_1)

    # void
    No_d = Node("d", [], is_end=True)
    No_i = Node("i", [No_d])
    No_o = Node("o", [No_i])
    No_v = Node("v", [No_o], is_start=True)
    keyword_tree.append(No_v)

    # repeat
    No_t = Node("t", [], is_end=True)
    No_a = Node("a", [No_t])
    No_e = Node("e", [No_a])
    No_p = Node("p", [No_e])
    No_e_1 = Node("e", [No_p])
    No_r = Node("r", [No_e_1], is_start=True)
    keyword_tree.append(No_r)

    # break
    No_k = Node("k", [], is_end=True)
    No_a = Node("a", [No_k])
    No_e = Node("e", [No_a])
    No_r = Node("r", [No_e])
    No_b = Node("b", [No_r], is_start=True)
    keyword_tree.append(No_b)

    # untill
    No_l = Node("l", [], is_end=True)
    No_l_1 = Node("l", [No_l])
    No_i = Node("i", [No_l_1])
    No_t = Node("t", [No_i])
    No_n = Node("n", [No_t])
    No_u = Node("u", [No_n], is_start=True)
    keyword_tree.append(No_u)

    # return
    No_n = Node("n", [], is_end=True)
    No_r = Node("r", [No_n])
    No_u = Node("u", [No_r])
    No_t = Node("t", [No_u])
    No_e = Node("e", [No_t])
    No_r_1 = Node("r", [No_e], is_start=True)
    keyword_tree.append(No_r_1)

    # Create identifier tree
    id_tree = []

    for i in range(11):
        exec(f'node_{i} = Node("{i}", [], is_end=True)', locals(), globals())
        exec(f"id_tree.append(node_{i})", locals(), globals())
    for alphabet in string.ascii_letters:
        exec(
            f'node_{alphabet} = Node("{alphabet}", [], is_start=True, is_end=True)',
            locals(),
            globals(),
        )
        exec(f"id_tree.append(node_{alphabet})", locals(), globals())

    for i in string.ascii_letters:
        exec(f"node_{i}.nexts = id_tree", locals(), globals())

    return [*symbol_tree, *whitespace_tree, *number_tree, *keyword_tree, *id_tree]


def get_next_char():
    global pointer, buffer

    pointer += 1
    with open("input.txt", "r") as file:
        char = file.read(pointer)
    buffer.append(char[pointer - 1 :])
    return char[pointer - 1 :]


def add_token_to_array(token) -> None:
    _type = ""
    for regex in TokenType:
        if re.search(regex.value, token):
            _type = regex

    if _type != "" and _type != TokenType.WHITESPACE:
        token_dict.setdefault(line_number, []).append(Token(_type.name, token))


def get_token_from_buffer():
    global buffer

    length = len(buffer) - 1
    token = buffer[:length]
    buffer = [buffer[length]]
    return "".join(token)


# global vars
token_dict: dict[int : List[Token]] = {}
line_number: int = 0
pointer = 0
buffer: List[str] = []


if __name__ == "__main__":
    dfa_tree = create_dfa_tree()
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
        selected_nodes = [node for node in dfa_tree if node.char == char]

        # Algorithm

        # No way to go in dfa tree --> possible token in buffer
        if len(selected_nodes) == 0:
            add_token_to_array(get_token_from_buffer())

        # Check if next character possibly can be append to our current state
        is_valid = False
        for option in selected_nodes:
            for node in option.nexts:
                if node.char == next_char:
                    is_valid = True
                    break
        if is_valid:
            char = next_char
            next_char = get_next_char()
        else:
            add_token_to_array(get_token_from_buffer())

        # next line
        if char == "\n":
            line_number += 1

    add_tokens_to_file(line_number, token_dict)
