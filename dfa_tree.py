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
    for i in [";", ":", ",", "[", "]", "(", ")", "{", "}", "+", "-", "*", "<"]:
        mother_state.next_edges.append(Edge(char=i, next_state=symbol_end_state))

    second_state_equal = State(next_edges=[], is_end=True)
    edge_equal = Edge(char="=", next_state=second_state_equal)
    first_state_equal = State(next_edges=[edge_equal])
    mother_state.next_edges.append(Edge(char="=", next_state=first_state_equal))


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
    number_end_state = State(
        is_end=True, invalid_next_pattern=f"[{string.ascii_letters}]+"
    )
    edge_number = Edge(pattern="[0-9]+", next_state=number_end_state)
    number_end_state.next_edges = [edge_number]
    mother_state.next_edges.append(edge_number)


def create_keyword_identifier_tree(mother_state):
    invalid_next_pattern = "[!]+"
    edge_letters_and_digits = Edge(
        pattern="[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789]+"
    )
    keyword_and_identifier_end_state = State(
        next_edges=[edge_letters_and_digits],
        is_end=True,
        invalid_next_pattern=invalid_next_pattern,
    )
    edge_letters_and_digits.next_state = keyword_and_identifier_end_state

    # Not keyword start character
    mother_state.next_edges.append(
        Edge(
            pattern="[acdfghjklmnopqstwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ]+",
            next_state=keyword_and_identifier_end_state,
        )
    )

    # Keyword start characters
    keyword_end_state = State(
        next_edges=[edge_letters_and_digits],
        is_end=True,
        invalid_next_pattern=invalid_next_pattern,
    )

    # Edges which is every letter except something
    edge_every_letter_except_t = Edge(
        pattern="[abcdefghijklmnopqrsuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789]+",
        next_state=keyword_and_identifier_end_state,
    )
    edge_every_letter_except_e = Edge(
        pattern="[abcdfghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789]+",
        next_state=keyword_and_identifier_end_state,
    )
    edge_every_letter_except_s = Edge(
        pattern="[abcdefghijklmnopqrtuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789]+",
        next_state=keyword_and_identifier_end_state,
    )
    edge_every_letter_except_l = Edge(
        pattern="[abcdefghijkmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789]+",
        next_state=keyword_and_identifier_end_state,
    )
    edge_every_letter_except_d = Edge(
        pattern="[abcefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789]+",
        next_state=keyword_and_identifier_end_state,
    )
    edge_every_letter_except_i = Edge(
        pattern="[abcdefghjklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789]+",
        next_state=keyword_and_identifier_end_state,
    )
    edge_every_letter_except_o = Edge(
        pattern="[abcdefghijklmnpqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789]+",
        next_state=keyword_and_identifier_end_state,
    )
    edge_every_letter_except_k = Edge(
        pattern="[abcdefghijlmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789]+",
        next_state=keyword_and_identifier_end_state,
    )
    edge_every_letter_except_a = Edge(
        pattern="[bcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789]+",
        next_state=keyword_and_identifier_end_state,
    )
    edge_every_letter_except_r = Edge(
        pattern="[abcdefghijklmnopqstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789]+",
        next_state=keyword_and_identifier_end_state,
    )
    edge_every_letter_except_t = Edge(
        pattern="[abcdefghijklmnopqrsuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789]+",
        next_state=keyword_and_identifier_end_state,
    )
    edge_every_letter_except_n = Edge(
        pattern="[abcdefghijklmopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789]+",
        next_state=keyword_and_identifier_end_state,
    )
    edge_every_letter_except_u = Edge(
        pattern="[abcdefghijklmnopqrstvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789]+",
        next_state=keyword_and_identifier_end_state,
    )
    edge_every_letter_except_t_and_p = Edge(
        pattern="[abcdefghijklmnoqrsuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789]+",
        next_state=keyword_and_identifier_end_state,
    )
    edge_every_letter_except_i_and_f = Edge(
        pattern="[abcdeghjklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789]+",
        next_state=keyword_and_identifier_end_state,
    )

    # else
    edge_e = Edge(char="e", next_state=keyword_end_state)

    s_next_state = State(
        next_edges=[edge_e, edge_every_letter_except_e],
        invalid_next_pattern=invalid_next_pattern,
    )

    edge_s = Edge(char="s", next_state=s_next_state)

    l_next_state = State(
        next_edges=[edge_s, edge_every_letter_except_s],
        invalid_next_pattern=invalid_next_pattern,
    )

    edge_l = Edge(char="l", next_state=l_next_state)

    e_next_state = State(
        next_edges=[edge_l, edge_every_letter_except_l],
        invalid_next_pattern=invalid_next_pattern,
    )
    mother_state.next_edges.append(Edge(char="e", next_state=e_next_state))

    # void
    edge_d = Edge(char="d", next_state=keyword_end_state)

    i_next_state = State(
        next_edges=[edge_d, edge_every_letter_except_d],
        invalid_next_pattern=invalid_next_pattern,
    )

    edge_i = Edge(char="i", next_state=i_next_state)

    o_next_state = State(
        next_edges=[edge_i, edge_every_letter_except_i],
        invalid_next_pattern=invalid_next_pattern,
    )

    edge_o = Edge(char="o", next_state=o_next_state)

    v_next_state = State(
        next_edges=[edge_o, edge_every_letter_except_o],
        invalid_next_pattern=invalid_next_pattern,
    )
    mother_state.next_edges.append(Edge(char="v", next_state=v_next_state))

    # break
    edge_k = Edge(char="k", next_state=keyword_end_state)

    k_next_state = State(
        next_edges=[edge_k, edge_every_letter_except_k],
        invalid_next_pattern=invalid_next_pattern,
    )

    edge_a = Edge(char="a", next_state=k_next_state)

    e_next_state = State(
        next_edges=[edge_a, edge_every_letter_except_a],
        invalid_next_pattern=invalid_next_pattern,
    )

    edge_e = Edge(char="e", next_state=e_next_state)

    r_next_state = State(
        next_edges=[edge_e, edge_every_letter_except_e],
        invalid_next_pattern=invalid_next_pattern,
    )

    edge_r = Edge(char="r", next_state=r_next_state)

    b_next_state = State(
        next_edges=[edge_r, edge_every_letter_except_r],
        invalid_next_pattern=invalid_next_pattern,
    )
    mother_state.next_edges.append(Edge(char="b", next_state=b_next_state))

    # until
    edge_l = Edge(char="l", next_state=keyword_end_state)

    i_next_state = State(
        next_edges=[edge_l, edge_every_letter_except_l],
        invalid_next_pattern=invalid_next_pattern,
    )

    edge_i = Edge(char="i", next_state=i_next_state)

    t_next_state = State(
        next_edges=[edge_i, edge_every_letter_except_i],
        invalid_next_pattern=invalid_next_pattern,
    )

    edge_t = Edge(char="t", next_state=t_next_state)

    n_next_state = State(
        next_edges=[edge_t, edge_every_letter_except_t],
        invalid_next_pattern=invalid_next_pattern,
    )

    edge_n = Edge(char="n", next_state=n_next_state)

    u_next_state = State(
        next_edges=[edge_n, edge_every_letter_except_n],
        invalid_next_pattern=invalid_next_pattern,
    )
    mother_state.next_edges.append(Edge(char="u", next_state=u_next_state))

    # if int
    edge_f = Edge(char="f", next_state=keyword_end_state)

    edge_t = Edge(char="t", next_state=keyword_end_state)

    t_next_state = State(
        next_edges=[edge_t, edge_every_letter_except_t],
        invalid_next_pattern=invalid_next_pattern,
    )

    edge_n = Edge(char="n", next_state=t_next_state)

    i_next_state = State(
        next_edges=[edge_n, edge_f, edge_every_letter_except_i_and_f],
        invalid_next_pattern=invalid_next_pattern,
    )
    mother_state.next_edges.append(Edge(char="i", next_state=i_next_state))

    # repeat return
    edge_t = Edge(char="t", next_state=keyword_end_state)

    a_next_state = State(
        next_edges=[edge_t, edge_every_letter_except_t],
        invalid_next_pattern=invalid_next_pattern,
    )
    edge_a = Edge(char="a", next_state=a_next_state)

    e_next_state = State(
        next_edges=[edge_a, edge_every_letter_except_a],
        invalid_next_pattern=invalid_next_pattern,
    )
    edge_e = Edge(char="e", next_state=e_next_state)

    p_next_state = State(
        next_edges=[edge_e, edge_every_letter_except_e],
        invalid_next_pattern=invalid_next_pattern,
    )
    edge_p = Edge(char="p", next_state=p_next_state)

    edge_n = Edge(char="n", next_state=keyword_end_state)

    n_next_state = State(
        next_edges=[edge_n, edge_every_letter_except_n],
        invalid_next_pattern=invalid_next_pattern,
    )
    edge_r = Edge(char="r", next_state=n_next_state)

    u_next_state = State(
        next_edges=[edge_r, edge_every_letter_except_r],
        invalid_next_pattern=invalid_next_pattern,
    )
    edge_u = Edge(char="u", next_state=u_next_state)

    t_next_state = State(
        next_edges=[edge_u, edge_every_letter_except_u],
        invalid_next_pattern=invalid_next_pattern,
    )
    edge_t = Edge(char="t", next_state=t_next_state)

    e_next_state = State(
        next_edges=[edge_t, edge_p, edge_every_letter_except_t_and_p],
        invalid_next_pattern=invalid_next_pattern,
    )
    edge_e = Edge(char="e", next_state=e_next_state)

    r_next_state = State(
        next_edges=[edge_e, edge_every_letter_except_e],
        invalid_next_pattern=invalid_next_pattern,
    )
    mother_state.next_edges.append(Edge(char="r", next_state=r_next_state))


def create_dfa_tree():
    mother_state = State()

    create_symbol_tree(mother_state)
    create_whitespace_tree(mother_state)
    create_digits_tree(mother_state)
    create_keyword_identifier_tree(mother_state)
    create_comment_tree(mother_state)

    return mother_state
