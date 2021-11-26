# def print_tree(graph, node, depth):
#     if depth == 0:
#         print(node)
#     elif depth == 1:
#         print("|---", node)
#     else:
#         print("|   ", "\t" * (depth - 2), "|---", node)
#     for i in graph[node]:
#         print_tree(graph, i, depth + 1)


from scanner import Token
from typing import List


class ParseTreeEdge:
    def __init__(
        self, next_node: "ParseTreeNode", terminal: str = None, non_terminal: str = None
    ):
        self.next_node = next_node
        self.terminal = terminal
        self.firsts: List[str] = None
        self.non_terminal = non_terminal

    def match(self, other, stack: List[str]):
        if self.non_terminal:
            return self.non_terminal == other
        elif other in self.firsts:
            stack.append(self.terminal)
            return True
        if self.terminal == "ε":
            return True


class ParseTreeNode:
    def __init__(self, next_edges: List[ParseTreeEdge] = []):
        self.next_edges = next_edges

    def next_parse_tree_node(self, other: str, stack: List[str]):
        for i in self.next_edges:
            if i.match(other, stack):
                return i.next_state
        if len(self.next_edges) == 0:
            stack.pop(len(stack) - 1)
            return None

    def __repr__(self):
        return f"ParseTreeNode<next_nodes = {self.next_edges}>"


first_dict = {}


def get_parse_tree():
    add_firsts()
    first_nodes = []

    # 1
    # end = ParseTreeNode(next_edges=[])
    # dollar = ParseTreeEdge(next_node=end, terminal="$")
    # dollar_node = ParseTreeNode(next_edges=[dollar])
    # declration_list = ParseTreeEdge(
    #     next_node=dollar_node, non_terminal="declration_list"
    # )
    # declration_list_node = ParseTreeNode(next_edges=[declration_list])
    # first_nodes.append(declration_list_node)

    # 2
    # end = ParseTreeNode(next_edges=[])
    # declration_list = ParseTreeEdge(next_node=end, non_terminal="declration_list")
    # declration_list_node = ParseTreeNode(next_edges=[declration_list])
    # declration = ParseTreeEdge(
    #     next_node=declration_list_node, non_terminal="declration"
    # )

    # epsilon_node = ParseTreeEdge(next_node=end, terminal="ε")

    # declration_node = ParseTreeNode(next_edges=[declration, epsilon_node])
    # first_nodes.append(declration_node)

    # 3
    # end = ParseTreeNode(next_edges=[])
    # declration_prime = ParseTreeEdge(next_node=end, non_terminal="declration_prime")
    # declration_prime_node = ParseTreeNode(next_edges=[declration_prime])
    # declration_initial = ParseTreeEdge(
    #     next_node=declration_prime_node, non_terminal="declration_initial"
    # )
    # declration_node = ParseTreeNode(next_edges=[declration_initial])
    # first_nodes.append(declration_node)

    # 4
    # end = ParseTreeNode(next_edges=[])
    # _id = ParseTreeEdge(next_node=end, terminal="ID")
    # id_node = ParseTreeNode(next_edges=[_id])
    # type_specifier = ParseTreeEdge(
    #     next_node=id_node, non_terminal="type_specifier"
    # )
    # type_specifier_node = ParseTreeNode(next_edges=[type_specifier])
    # first_nodes.append(type_specifier_node)

    # 5
    # end = ParseTreeNode(next_edges=[])
    # fun_declartion_prime = ParseTreeEdge(
    #     next_node=end, non_terminal="fun_declartion_prime"
    # )

    # var_declartion_prime = ParseTreeEdge(
    #     next_node=end, non_terminal="var_declartion_prime"
    # )

    # start_node = ParseTreeNode(next_edges=[fun_declartion_prime, var_declartion_prime])
    # first_nodes.append(start_node)

    # 6
    # end = ParseTreeNode(next_edges=[])

    # semicolon = ParseTreeEdge(next_node=end, terminal=";")

    # semicolon_2 = ParseTreeEdge(next_node=end, terminal=";")
    # semicolon_2_node = ParseTreeNode(next_edges=[semicolon_2])
    # close_t = ParseTreeEdge(next_node=semicolon_2_node, terminal="]")
    # num_node = ParseTreeNode(next_edges=[close_t])
    # num = ParseTreeEdge(next_node=num_node, terminal="NUM")
    # open_t_node = ParseTreeNode(next_edges=[num])
    # open_t = ParseTreeEdge(next_node=open_t_node, terminal="[")

    # start_node = ParseTreeNode(next_edges=[semicolon, open_t])
    # first_nodes.append(start_node)

    # 7
    # end = ParseTreeNode(next_edges=[])
    # compound_stmt = ParseTreeEdge(next_node=end, non_terminal="compound_stmt")
    # compound_stmt_node = ParseTreeNode(next_edges=[compound_stmt])
    # close_par = ParseTreeEdge(next_node=compound_stmt_node, terminal=")")
    # close_par_node = ParseTreeNode(next_edges=[close_par])
    # params = ParseTreeEdge(next_node=close_par_node, non_terminal="params")
    # params_node = ParseTreeNode(next_edges=[params])
    # open_par = ParseTreeEdge(next_node=params_node, terminal="(")
    # first_nodes.append(open_par)

    # 8
    # end = ParseTreeNode(next_edges=[])
    # _int = ParseTreeEdge(next_node=end, terminal="int")

    # _void = ParseTreeEdge(next_node=end, terminal="void")

    # start_node = ParseTreeNode(next_edges=[_int, _void])
    # first_nodes.append(start_node)

    return


def add_firsts():
    with open("firsts.txt", "r") as file:
        a = list(map(str.split, file.readlines()))
    for line in a:
        first_dict[line[0]] = line[1:]
