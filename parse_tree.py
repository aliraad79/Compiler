graph = {
    "A": ["B", "C"],
    "B": ["D"],
    "C": ["E", "F"],
    "D": ["G", "H"],
    "F": ["I", "J", "K"],
    "E": [],
    "G": [],
    "J": [],
    "K": [],
    "H": [],
    "I": [],
}

def print_tree(graph, node, depth):
    if depth == 0:
        print(node)
    elif depth == 1:
        print("|---", node)
    else:
        print("|   ", "\t" * (depth - 2), "|---", node)
    for i in graph[node]:
        print_tree(graph, i, depth + 1)


print_tree(graph, "A", 0)
