from typing import List
import re


class Edge:
    def __init__(
        self,
        next_state: "State" = None,
        char: str = "",
        pattern: str = "",
    ):
        self.next_state = next_state
        self.char = char
        self.pattern = pattern

    @property
    def is_pattern_state(self):
        return self.pattern != ""

    def __repr__(self):
        if self.is_pattern_state:
            return f"Edge with pattern = {repr(self.pattern)}"
        return f"Edge with char = {repr(self.char)}"


class State:
    def __init__(self, next_edges: List[Edge] = []):
        self.next_edges = next_edges

    def next_dfa_tree_state(self, other: str):
        for i in self.next_edges:
            if i.is_pattern_state and re.match(i.pattern, other):
                return i.next_state
            elif i.char != "" and i.char == other:
                return i.next_state

    def __repr__(self):
        return "State<>"


def create_symbol_tree(mother_state: State):
    error_state = State(next_edges=[])
    error_edge = Edge(char="#", next_state=error_state)
    symbol_end_state = State(next_edges=[])
    for i in [";", ":", ",", "[", "]", "(", ")", "{", "}", "+", "-", "<"]:
        mother_state.next_edges.append(Edge(char=i, next_state=symbol_end_state))

    second_state_equal = State(next_edges=[])
    edge_equal = Edge(char="=", next_state=second_state_equal)
    first_state_equal = State(next_edges=[edge_equal, error_edge])
    mother_state.next_edges.append(Edge(char="=", next_state=first_state_equal))

    state_unmatch_comment = State(next_edges=[])
    state_star = State(
        next_edges=[Edge(char="/", next_state=state_unmatch_comment), error_edge]
    )
    mother_state.next_edges.append(Edge(char="*", next_state=state_star))


def create_whitespace_tree(mother_state):
    whitespace_end_state = State(next_edges=[])
    white_spaces = ["\x09", "\x0A", "\x0B", "\x0C", "\x20"]
    for i in white_spaces:
        mother_state.next_edges.append(Edge(char=i, next_state=whitespace_end_state))


def create_comment_tree(mother_state):
    comment_end_state = State(next_edges=[])

    # /* . */
    edge_slash = Edge(char="/", next_state=comment_end_state)

    edge_every_letter_except_star_and_slash = Edge(pattern="[^*\/]+")

    edge_star = Edge(char="*")
    state_second_star = State(
        next_edges=[edge_star, edge_slash, edge_every_letter_except_star_and_slash],
    )
    edge_star.next_state = state_second_star

    edge_star = Edge(char="*", next_state=state_second_star)

    edge_everything_but_star = Edge(pattern="[^*]+")

    state_everything_but_star = State(next_edges=[edge_everything_but_star, edge_star])

    edge_everything_but_star.next_state = state_everything_but_star

    edge_every_letter_except_star_and_slash.next_state = state_everything_but_star

    edge_slash_star = Edge(char="*", next_state=state_everything_but_star)

    # //
    edge_new_line = Edge(char="\n", next_state=comment_end_state)

    edge_everything_but_newline = Edge(pattern="[^\n]+")

    state_in_comment = State(next_edges=[edge_everything_but_newline, edge_new_line])

    edge_everything_but_newline.next_state = state_in_comment

    edge_double_slash = Edge(char="/", next_state=state_in_comment)

    state_start_slash = State(next_edges=[edge_double_slash, edge_slash_star])
    mother_state.next_edges.append(Edge(char="/", next_state=state_start_slash))


def create_digits_tree(mother_state):
    number_error_state = State(next_edges=[])
    edge_error = Edge(pattern="[a-zA-Z]+", next_state=number_error_state)

    number_end_state = State()
    edge_number = Edge(pattern="[0-9]+", next_state=number_end_state)
    number_end_state.next_edges = [edge_number, edge_error]
    mother_state.next_edges.append(edge_number)


def create_keyword_identifier_tree(mother_state):
    error_state = State(next_edges=[])
    error_edge = Edge(
        pattern="[^a-zA-Z0-9\x09\x0A\x0B\x0C\x20;:,\[\]\(\)\{\}\+\-\<]",
        next_state=error_state,
    )

    edge_letters_and_digits = Edge(pattern="[a-zA-Z0-9]")
    main_state = State(next_edges=[edge_letters_and_digits, error_edge])

    edge_letters_and_digits.next_state = main_state

    mother_state.next_edges.append(Edge(pattern="[a-zA-Z]", next_state=main_state))


def create_dfa_tree():
    mother_state = State()

    create_symbol_tree(mother_state)
    create_whitespace_tree(mother_state)
    create_digits_tree(mother_state)
    create_keyword_identifier_tree(mother_state)
    create_comment_tree(mother_state)

    return mother_state
