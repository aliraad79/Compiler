# graph = {
#     "A": ["B", "C"],
#     "B": ["D"],
#     "C": ["E", "F"],
#     "D": ["G", "H"],
#     "F": ["I", "J", "K"],
#     "E": [],
#     "G": [],
#     "J": [],
#     "K": [],
#     "H": [],
#     "I": [],
# }

# def print_tree(graph, node, depth):
#     if depth == 0:
#         print(node)
#     elif depth == 1:
#         print("|---", node)
#     else:
#         print("|   ", "\t" * (depth - 2), "|---", node)
#     for i in graph[node]:
#         print_tree(graph, i, depth + 1)


# print_tree(graph, "A", 0)
from scanner import Token
from typing import List


class ParseTreeEdge:
    def __init__(
        self,
        next_node: "ParseTreeNode" = None,
        token: Token = None,
        
    ):
        self.next_node = next_node
        self.token = token

    def __repr__(self):
        return f"Edge<next_node = {self.next_node}, token = {self.token}>"


class ParseTreeNode:
    def __init__(self, next_nodes: List[ParseTreeEdge] = []):
        self.next_nodes = next_nodes

    def next_parse_state(self, other: Token):
        for i in self.next_nodes:
            if i.token == other:
                return i

    def __repr__(self):
        return f"ParseTreeNode<next_nodes = {self.next_nodes}>"


def get_parse_tree():
    program = ParseTreeNode()
    
    declaration_list_node = None
    declaration_list = ParseTreeEdge(declaration_list_node,)

    program.next_nodes.append(declaration_list)
    return
