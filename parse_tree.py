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


class ParseTreeNode:
    def __init__(self, next_nodes: List["ParseTreeNode"] = []):
        self.next_nodes = next_nodes

    def __repr__(self):
        return f"ParseTreeNode<next_nodes = {self.next_nodes}>"


class Terminal(ParseTreeNode):
    def next_parse_state(self, other: Token):
        for i in self.next_edges:
            if i.token == other:
                return i


class NonTerminal(ParseTreeNode):
    ...


def get_parse_tree():
    o = []
    with open('firsts.txt', 'r') as file:
        a = list(map(str.split,file.readlines()))
    for i in a:
        o.append(NonTerminal())
    program = ParseTreeNode()



    program.next_nodes.append(declaration_list)
    return
