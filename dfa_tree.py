from compiler import Node
import string


def create_symbol_tree():
    tree = []
    for i in [";", ":", ",", "[", "]", "(", ")", "{", "}", "+", "-", "*", "<"]:
        tree.append(Node(i, [], is_start=True, is_end=True))

    # Add == to symbol tree
    node_equal = Node("=", [], is_end=True)
    tree.append(Node("=", [node_equal], is_start=True, is_end=True))

    return tree


def create_whitespace_tree():
    tree = []
    white_spaces = ["\x09", "\x0A", "\x0B", "\x0C", "\x20"]
    for i in white_spaces:
        tree.append(Node(i, [], is_start=True, is_end=True))

    return tree


def create_number_tree():
    for i in range(10):
        exec(
            f'node_{i} = Node("{i}", [], is_start=True, is_end=True)',
            locals(),
            globals(),
        )
    all_numbers = [
        node_0,
        node_1,
        node_2,
        node_3,
        node_4,
        node_5,
        node_6,
        node_7,
        node_8,
        node_9,
    ]
    node_0.nexts = all_numbers
    node_1.nexts = all_numbers
    node_2.nexts = all_numbers
    node_3.nexts = all_numbers
    node_4.nexts = all_numbers
    node_5.nexts = all_numbers
    node_6.nexts = all_numbers
    node_7.nexts = all_numbers
    node_8.nexts = all_numbers
    node_9.nexts = all_numbers
    return [
        node_0,
        node_1,
        node_2,
        node_3,
        node_4,
        node_5,
        node_6,
        node_7,
        node_8,
        node_9,
    ]


def create_keyword_tree():
    tree = []
    # if
    Node_f = Node("f", [], is_end=True)
    Node_i = Node("i", [Node_f], is_start=True)
    tree.append(Node_i)

    # int
    Node_t = Node("t", [], is_end=True)
    Node_n = Node("n", [Node_t])
    Node_i = Node("i", [Node_n], is_start=True)
    tree.append(Node_i)

    # else
    Node_e = Node("e", [], is_end=True)
    Node_s = Node("s", [Node_e])
    Node_l = Node("l", [Node_s])
    Node_e_1 = Node("e", [Node_l], is_start=True)
    tree.append(Node_e_1)

    # void
    Node_d = Node("d", [], is_end=True)
    Node_i = Node("i", [Node_d])
    Node_o = Node("o", [Node_i])
    Node_v = Node("v", [Node_o], is_start=True)
    tree.append(Node_v)

    # repeat
    Node_t = Node("t", [], is_end=True)
    Node_a = Node("a", [Node_t])
    Node_e = Node("e", [Node_a])
    Node_p = Node("p", [Node_e])
    Node_e_1 = Node("e", [Node_p])
    Node_r = Node("r", [Node_e_1], is_start=True)
    tree.append(Node_r)

    # break
    Node_k = Node("k", [], is_end=True)
    Node_a = Node("a", [Node_k])
    Node_e = Node("e", [Node_a])
    Node_r = Node("r", [Node_e])
    Node_b = Node("b", [Node_r], is_start=True)
    tree.append(Node_b)

    # until
    Node_l = Node("l", [], is_end=True)
    Node_i = Node("i", [Node_l])
    Node_t = Node("t", [Node_i])
    Node_n = Node("n", [Node_t])
    Node_u = Node("u", [Node_n], is_start=True)
    tree.append(Node_u)

    # return
    Node_n = Node("n", [], is_end=True)
    Node_r = Node("r", [Node_n])
    Node_u = Node("u", [Node_r])
    Node_t = Node("t", [Node_u])
    Node_e = Node("e", [Node_t])
    Node_r_1 = Node("r", [Node_e], is_start=True)
    tree.append(Node_r_1)
    return tree


def create_comment_tree():
    # /* . */
    Node_slash_2 = Node("/", [], is_end=True)
    Node_star_2 = Node("*", is_universal=True)
    Node_star_2.nexts = [Node_star_2]
    Node_star_2.next_universal_nodes = [Node_slash_2]

    Node_star = Node("*", is_universal=True)
    Node_star.nexts = [Node_star]
    Node_star.next_universal_nodes = [Node_star_2]

    # //
    node_new_line = Node("\n", [], is_end=True)
    Node_slash = Node("/", is_universal=True, next_universal_nodes=[node_new_line])
    Node_slash.nexts = [Node_slash]

    Node_start_slash = Node("/", [Node_slash, Node_star], is_start=True)
    return [Node_start_slash]


def create_dfa_tree():
    symbol_tree = create_symbol_tree()
    whitespace_tree = create_whitespace_tree()
    number_tree = create_number_tree()
    keyword_tree = create_keyword_tree()
    comment_tree = create_comment_tree()

    # Create identifier tree
    id_tree = []
    middle_tree = []

    for i in range(11):
        exec(f'node_{i} = Node("{i}", [], is_end=True)', locals(), globals())
        exec(f"middle_tree.append(node_{i})", locals(), globals())
    for alphabet in string.ascii_letters:
        exec(
            f'node_{alphabet} = Node("{alphabet}", [], is_start=True, is_end=True)',
            locals(),
            globals(),
        )
        exec(f"middle_tree.append(node_{alphabet})", locals(), globals())

    for i in string.ascii_letters:
        exec(f"node_{i}.nexts = middle_tree", locals(), globals())
        exec(f"id_tree.append(node_{i})", locals(), globals())

    return [
        *symbol_tree,
        *whitespace_tree,
        *number_tree,
        *keyword_tree,
        *id_tree,
        *comment_tree,
    ]
