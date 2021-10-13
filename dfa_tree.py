from typing import List
import re
import string


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
            return f"Edge with next state = {self.next_state} with some pattern"
        return f"Edge next state = {self.next_state} with char = {repr(self.char)}"


class State:
    def __init__(
        self,
        next_edges: List[Edge] = [],
        is_end: bool = False,
        invalid_next_pattern: str = "",
    ):
        self.next_edges = next_edges
        self.is_end = is_end
        self.invalid_next_pattern = invalid_next_pattern

    def next_dfa_tree_state(self, other: str):
        for i in self.next_edges:
            if i.is_pattern_state and re.match(i.pattern, other):
                return i.next_state
            elif i.char == other:
                return i.next_state

    def __repr__(self):
        return f"State <end={self.is_end}>"


def create_symbol_tree(mother_state: State):
    symbol_end_state = State(next_edges=[], is_end=True)
    for i in [";", ":", ",", "[", "]", "(", ")", "{", "}", "+", "-", "<"]:
        mother_state.next_edges.append(Edge(char=i, next_state=symbol_end_state))

    second_state_equal = State(next_edges=[], is_end=True)
    edge_equal = Edge(char="=", next_state=second_state_equal)
    first_state_equal = State(next_edges=[edge_equal])
    mother_state.next_edges.append(Edge(char="=", next_state=first_state_equal))

    state_unmatch_comment = State(next_edges=[], is_end=True)
    state_star = State(
        next_edges=[Edge(char="/", next_state=state_unmatch_comment)], is_end=True
    )
    mother_state.next_edges.append(Edge(char="*", next_state=state_star))


def create_whitespace_tree(mother_state):
    whitespace_end_state = State(next_edges=[], is_end=True)
    white_spaces = ["\x09", "\x0A", "\x0B", "\x0C", "\x20"]
    for i in white_spaces:
        mother_state.next_edges.append(Edge(char=i, next_state=whitespace_end_state))


def create_comment_tree(mother_state):
    comment_end_state = State(next_edges=[], is_end=True)

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

    edge_slash_start = Edge(char="*", next_state=state_everything_but_star)

    # //
    edge_new_line = Edge(char="\n", next_state=comment_end_state)
    double_slash_loop_state = State()

    edge_everything_but_newline = Edge(
        pattern="[^\n]+", next_state=double_slash_loop_state
    )

    double_slash_loop_state.next_state = edge_everything_but_newline

    state_in_comment = State(next_edges=[edge_everything_but_newline, edge_new_line])

    edge_double_slash = Edge(char="/", next_state=state_in_comment)

    state_start_slash = State(next_edges=[edge_double_slash, edge_slash_start])
    mother_state.next_edges.append(Edge(char="/", next_state=state_start_slash))


def create_digits_tree(mother_state):
    number_error_state = State(
        is_end=True, invalid_next_pattern=f"[{string.ascii_letters}]+"
    )
    edge_error = Edge(
        pattern="[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ]+",
        next_state=number_error_state,
    )
    number_error_state.next_edges = [edge_error]

    number_end_state = State(
        is_end=True, invalid_next_pattern=f"[{string.ascii_letters}]+"
    )
    edge_number = Edge(pattern="[0-9]+", next_state=number_end_state)
    number_end_state.next_edges = [edge_number, edge_error]
    mother_state.next_edges.append(edge_number)


def create_keyword_identifier_tree(mother_state):
    edge_letters_and_digits = Edge(
        pattern="[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789]"
    )

    main_state = State(next_edges=[edge_letters_and_digits])

    edge_letters_and_digits.next_state = main_state

    mother_state.next_edges.append(
        Edge(
            pattern="[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ]",
            next_state=main_state,
        )
    )


def create_dfa_tree():
    mother_state = State()

    create_symbol_tree(mother_state)
    create_whitespace_tree(mother_state)
    create_digits_tree(mother_state)
    create_keyword_identifier_tree(mother_state)
    create_comment_tree(mother_state)

    return mother_state
