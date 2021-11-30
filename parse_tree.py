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

    def match(self, other):
        if self.non_terminal:
            return other in first_dict[self.non_terminal]
        elif self.terminal:
            return other == self.terminal
        if self.terminal == "ε":
            return True

    def __repr__(self):
        return f"Edge<{self.terminal if self.terminal else self.non_terminal}>"


class ParseTreeNode:
    def __init__(self, next_edges: List[ParseTreeEdge] = []):
        self.next_edges = next_edges

    def next_parse_tree_node(self, other: str):
        for i in self.next_edges:
            if i.match(other):
                return i.next_node, i.terminal != None
        if len(self.next_edges) == 0:
            return None, False
        print("wtf ", self.next_edges)

    def __repr__(self):
        return f"ParseTreeNode<next_edges = {self.next_edges}>"


first_dict = {}


def init_transation_diagrams():
    add_firsts()
    first_nodes = {
        "program": program_diagram(),
        "declaration_list": declaration_list_diagram(),
        "declaration": declaration_diagram(),
        "declaration_initial": declaration_initial_diagram(),
        "declaration_prime": declaration_prime_diagram(),
        "var_declarion_prime": var_declarion_prime_diagram(),
        "fun_declaration_prime": fun_declaration_prime(),
        "type_specifier": type_specifier_diagram(),
        "params": params_diagram(),
        "param_list": param_list_diagram(),
        "param": param_diagram(),
        "param_prime": param_prime_diagram(),
        "compund_stmt": compund_stmt(),
        "statement_list": statement_list_diagram(),
        "statement": statement_diagram(),
        "expression_stmt": expression_stmt_diagram(),
        "selection_stmt": selection_stmt_diagram(),
        "else_stmt": else_stmt_diagram(),
        "iteration_stmt": iteration_stmt_diagram(),
        "return_stmt": return_stmt_diagram(),
        "return_stmt_prime": return_stmt_prime_diagram(),
        "expression": expression_diagram(),
        "B": B_diagram(),
        "H": H_diagram(),
        "simple_expression_zegond": simple_expression_zegond_diagram(),
        "simple_expression_prime": simple_expression_prime_diagram(),
        "C": C_diagram(),
        "relop": relop_diagram(),
        "additive_expression": additive_expression_diagram(),
        "additive_expression_prime": additive_expression_prime_diagram(),
        "additive_expression_zegond": additive_expression_zegond_diagram(),
        "D": D_diagram(),
        "addop": addop_diagram(),
        "term": term_diagram(),
        "term_prime": term_prime_diagram(),
        "term_zegond": term_zegond_diagram(),
        "G": G_diagram(),
        "factor": factor_diagram(),
        "var_call_prime": var_call_prime_diagram(),
        "var_prime": var_prime_diagram(),
        "factor_prime": factor_prime_diagram(),
        "factor_zegond": factor_zegond_diagram(),
        "args": args_diagram(),
        "arg_list": arg_list_diagram(),
        "arg_list_prime": arg_list_prime_diagram(),
    }
    return first_nodes


def arg_list_prime_diagram():
    end = ParseTreeNode(next_edges=[])
    arg_list_prime = ParseTreeEdge(next_node=end, non_terminal="arg_list_prime")
    arg_list_prime_node = ParseTreeNode(next_edges=[arg_list_prime])
    expression = ParseTreeEdge(next_node=arg_list_prime_node, non_terminal="expression")
    expression_node = ParseTreeNode(next_edges=[expression])
    comma = ParseTreeEdge(next_node=expression_node, terminal=",")

    epsilon_node = ParseTreeEdge(next_node=end, terminal="ε")

    return ParseTreeNode(next_edges=[comma, epsilon_node])


def arg_list_diagram():
    end = ParseTreeNode(next_edges=[])
    arg_list_prime = ParseTreeEdge(next_node=end, non_terminal="arg_list_prime")
    arg_list_prime_node = ParseTreeNode(next_edges=[arg_list_prime])
    expression = ParseTreeEdge(next_node=arg_list_prime_node, non_terminal="expression")

    return ParseTreeNode(next_edges=[expression])


def args_diagram():
    end = ParseTreeNode(next_edges=[])
    arg_list = ParseTreeEdge(next_node=end, non_terminal="arg_list")

    epsilon_node = ParseTreeEdge(next_node=end, terminal="ε")

    return ParseTreeNode(next_edges=[arg_list, epsilon_node])


def factor_zegond_diagram():
    end = ParseTreeNode(next_edges=[])
    close_par = ParseTreeEdge(next_node=end, terminal=")")
    close_par_node = ParseTreeNode(next_edges=[close_par])
    expression = ParseTreeEdge(next_node=close_par_node, non_terminal="expression")
    expression_node = ParseTreeNode(next_edges=[expression])
    open_par = ParseTreeEdge(next_node=expression_node, terminal="(")

    num = ParseTreeEdge(next_node=end, terminal="NUM")

    return ParseTreeNode(next_edges=[open_par, num])


def factor_prime_diagram():
    end = ParseTreeNode(next_edges=[])
    close_par = ParseTreeEdge(next_node=end, terminal=")")
    close_par_node = ParseTreeNode(next_edges=[close_par])
    args = ParseTreeEdge(next_node=close_par_node, non_terminal="args")
    args_node = ParseTreeNode(next_edges=[args])
    open_par = ParseTreeEdge(next_node=args_node, terminal="(")

    epsilon_node = ParseTreeEdge(next_node=end, terminal="ε")

    return ParseTreeNode(next_edges=[open_par, epsilon_node])


def var_prime_diagram():
    end = ParseTreeNode(next_edges=[])
    close_par = ParseTreeEdge(next_node=end, terminal="]")
    close_par_node = ParseTreeNode(next_edges=[close_par])
    expression = ParseTreeEdge(next_node=close_par_node, non_terminal="expression")
    expression_node = ParseTreeNode(next_edges=[expression])
    open_par = ParseTreeEdge(next_node=expression_node, terminal="[")

    epsilon_node = ParseTreeEdge(next_node=end, terminal="ε")

    return ParseTreeNode(next_edges=[open_par, epsilon_node])


def var_call_prime_diagram():
    end = ParseTreeNode(next_edges=[])
    close_par = ParseTreeEdge(next_node=end, terminal=")")
    close_par_node = ParseTreeNode(next_edges=[close_par])
    args = ParseTreeEdge(next_node=close_par_node, non_terminal="args")
    args_node = ParseTreeNode(next_edges=[args])
    open_par = ParseTreeEdge(next_node=args_node, terminal="(")

    var_prime = ParseTreeEdge(next_node=end, non_terminal="var_prime")

    return ParseTreeNode(next_edges=[open_par, var_prime])


def factor_diagram():
    end = ParseTreeNode(next_edges=[])
    close_par = ParseTreeEdge(next_node=end, terminal=")")
    close_par_node = ParseTreeNode(next_edges=[close_par])
    expression = ParseTreeEdge(next_node=close_par_node, non_terminal="expression")
    expression_node = ParseTreeNode(next_edges=[expression])
    open_par = ParseTreeEdge(next_node=expression_node, terminal="(")

    var_call_prime = ParseTreeEdge(next_node=end, non_terminal="var_call_prime")
    var_call_prime_node = ParseTreeNode(next_edges=[var_call_prime])
    id = ParseTreeEdge(next_node=var_call_prime_node, terminal="ID")

    num = ParseTreeEdge(next_node=end, terminal="NUM")

    return ParseTreeNode(next_edges=[open_par, num, id])


def G_diagram():
    end = ParseTreeNode(next_edges=[])
    _G_edge = ParseTreeEdge(next_node=end, non_terminal="G")
    _G_node = ParseTreeNode(next_edges=[_G_edge])
    factor = ParseTreeEdge(next_node=_G_node, non_terminal="factor")
    factor_node = ParseTreeNode(next_edges=[factor])
    star = ParseTreeEdge(next_node=factor_node, terminal="*")

    epsilon_node = ParseTreeEdge(next_node=end, terminal="ε")

    return ParseTreeNode(next_edges=[star, epsilon_node])


def term_zegond_diagram():
    end = ParseTreeNode(next_edges=[])
    _G_edge = ParseTreeEdge(next_node=end, non_terminal="G")
    _G_node = ParseTreeNode(next_edges=[_G_edge])
    factor_zegond = ParseTreeEdge(next_node=_G_node, non_terminal="factor_zegond")

    return ParseTreeNode(next_edges=[factor_zegond])


def term_prime_diagram():
    end = ParseTreeNode(next_edges=[])
    _G_edge = ParseTreeEdge(next_node=end, non_terminal="G")
    _G_node = ParseTreeNode(next_edges=[_G_edge])
    factor_prime = ParseTreeEdge(next_node=_G_node, non_terminal="factor_prime")

    return ParseTreeNode(next_edges=[factor_prime])


def term_diagram():
    end = ParseTreeNode(next_edges=[])
    _G_edge = ParseTreeEdge(next_node=end, non_terminal="G")
    _G_node = ParseTreeNode(next_edges=[_G_edge])
    factor = ParseTreeEdge(next_node=_G_node, non_terminal="factor")

    return ParseTreeNode(next_edges=[factor])


def addop_diagram():
    end = ParseTreeNode(next_edges=[])
    plus = ParseTreeEdge(next_node=end, terminal="+")

    minus = ParseTreeEdge(next_node=end, terminal="-")

    return ParseTreeNode(next_edges=[plus, minus])


def D_diagram():
    end = ParseTreeNode(next_edges=[])
    _D_edge = ParseTreeEdge(next_node=end, non_terminal="D")
    _D_node = ParseTreeNode(next_edges=[_D_edge])
    term = ParseTreeEdge(next_node=_D_node, non_terminal="term")
    term_node = ParseTreeNode(next_edges=[term])
    addop = ParseTreeEdge(next_node=term_node, non_terminal="addop")

    epsilon_node = ParseTreeEdge(next_node=end, terminal="ε")

    return ParseTreeNode(next_edges=[addop, epsilon_node])


def additive_expression_zegond_diagram():
    end = ParseTreeNode(next_edges=[])
    _D_edge = ParseTreeEdge(next_node=end, non_terminal="D")
    _D_node = ParseTreeNode(next_edges=[_D_edge])
    term_zegond = ParseTreeEdge(next_node=_D_node, non_terminal="term_zegond")

    return ParseTreeNode(next_edges=[term_zegond])


def additive_expression_prime_diagram():
    end = ParseTreeNode(next_edges=[])
    _D_edge = ParseTreeEdge(next_node=end, non_terminal="D")
    _D_node = ParseTreeNode(next_edges=[_D_edge])
    term_prime = ParseTreeEdge(next_node=_D_node, non_terminal="term_prime")

    return ParseTreeNode(next_edges=[term_prime])


def additive_expression_diagram():
    end = ParseTreeNode(next_edges=[])
    _D_edge = ParseTreeEdge(next_node=end, non_terminal="D")
    _D_node = ParseTreeNode(next_edges=[_D_edge])
    term = ParseTreeEdge(next_node=_D_node, non_terminal="term")

    return ParseTreeNode(next_edges=[term])


def relop_diagram():
    end = ParseTreeNode(next_edges=[])
    lower = ParseTreeEdge(next_node=end, terminal="<")

    equal_1 = ParseTreeEdge(next_node=end, terminal="=")
    equal_1_node = ParseTreeNode(next_edges=[equal_1])
    equal_2 = ParseTreeEdge(next_node=equal_1_node, terminal="=")

    return ParseTreeNode(next_edges=[lower, equal_2])


def C_diagram():
    end = ParseTreeNode(next_edges=[])
    additive_expression = ParseTreeEdge(
        next_node=end, non_terminal="additive_expression"
    )
    additive_expression_node = ParseTreeNode(next_edges=[additive_expression])
    relop = ParseTreeEdge(next_node=additive_expression_node, non_terminal="relop")

    epsilon_node = ParseTreeEdge(next_node=end, terminal="ε")

    return ParseTreeNode(next_edges=[relop, epsilon_node])


def simple_expression_prime_diagram():
    end = ParseTreeNode(next_edges=[])
    _C_edge = ParseTreeEdge(next_node=end, non_terminal="C")
    _C_node = ParseTreeNode(next_edges=[_C_edge])
    additive_expression_prime = ParseTreeEdge(
        next_node=_C_node, non_terminal="additive_expression_prime"
    )

    return ParseTreeNode(next_edges=[additive_expression_prime])


def simple_expression_zegond_diagram():
    end = ParseTreeNode(next_edges=[])
    _C_edge = ParseTreeEdge(next_node=end, non_terminal="C")
    _C_node = ParseTreeNode(next_edges=[_C_edge])
    additive_expression_zegond = ParseTreeEdge(
        next_node=_C_node, non_terminal="additive_expression_zegond"
    )

    return ParseTreeNode(next_edges=[additive_expression_zegond])


def H_diagram():
    end = ParseTreeNode(next_edges=[])
    _C_edge = ParseTreeEdge(next_node=end, non_terminal="C")
    _C_node = ParseTreeNode(next_edges=[_C_edge])
    _D_edge = ParseTreeEdge(next_node=_C_node, non_terminal="D")
    _D_node = ParseTreeNode(next_edges=[_D_edge])
    _G_edge = ParseTreeEdge(next_node=_D_node, non_terminal="G")

    expression = ParseTreeEdge(next_node=end, non_terminal="expression")

    return ParseTreeNode(next_edges=[expression, _G_edge])


def B_diagram():
    end = ParseTreeNode(next_edges=[])

    _H_edge = ParseTreeEdge(next_node=end, non_terminal="H")
    _H_node = ParseTreeNode(next_edges=[_H_edge])
    close_par = ParseTreeEdge(next_node=_H_node, terminal="]")
    close_par_node = ParseTreeNode(next_edges=[close_par])
    expression = ParseTreeEdge(next_node=close_par_node, non_terminal="expression")
    expression_node = ParseTreeNode(next_edges=[expression])
    open_par = ParseTreeEdge(next_node=expression_node, terminal="[")

    expression_2 = ParseTreeEdge(next_node=end, non_terminal="expression")

    simple_expression_prime = ParseTreeEdge(
        next_node=end, non_terminal="simple_expression_prime"
    )

    return ParseTreeNode(next_edges=[simple_expression_prime, expression_2, open_par])


def expression_diagram():
    end = ParseTreeNode(next_edges=[])
    _B_edge = ParseTreeEdge(next_node=end, non_terminal="B")
    _B_node = ParseTreeNode(next_edges=[_B_edge])
    _id = ParseTreeEdge(next_node=_B_node, terminal="ID")

    simple_expression_zegond = ParseTreeEdge(
        next_node=end, non_terminal="simple_expression_zegond"
    )

    return ParseTreeNode(next_edges=[simple_expression_zegond, _id])


def return_stmt_prime_diagram():
    end = ParseTreeNode(next_edges=[])

    semicolon_2 = ParseTreeEdge(next_node=end, terminal=";")
    semicolon_2_node = ParseTreeNode(next_edges=[semicolon_2])
    expression = ParseTreeEdge(next_node=semicolon_2_node, non_terminal="expression")

    semicolon = ParseTreeEdge(next_node=end, terminal=";")

    return ParseTreeNode(next_edges=[semicolon, expression])


def return_stmt_diagram():
    end = ParseTreeNode(next_edges=[])
    return_stmt_prime = ParseTreeEdge(next_node=end, non_terminal="return_stmt_prime")
    statement_node = ParseTreeNode(next_edges=[return_stmt_prime])
    _return = ParseTreeEdge(next_node=statement_node, terminal="return")

    return ParseTreeNode(next_edges=[_return])


def iteration_stmt_diagram():
    end = ParseTreeNode(next_edges=[])
    close_bracket = ParseTreeEdge(next_node=end, terminal=")")
    close_bracket_node = ParseTreeNode(next_edges=[close_bracket])
    expression = ParseTreeEdge(next_node=close_bracket_node, non_terminal="expression")
    expression_node = ParseTreeNode(next_edges=[expression])
    open_bracket = ParseTreeEdge(next_node=expression_node, terminal="(")
    open_bracket_node = ParseTreeNode(next_edges=[open_bracket])
    until = ParseTreeEdge(next_node=open_bracket_node, terminal="until")
    until_node = ParseTreeNode(next_edges=[until])
    statement = ParseTreeEdge(next_node=until_node, non_terminal="statement")
    statement_node = ParseTreeNode(next_edges=[statement])
    repeat = ParseTreeEdge(next_node=statement_node, terminal="repeat")

    return ParseTreeNode(next_edges=[repeat])


def else_stmt_diagram():
    end = ParseTreeNode(next_edges=[])
    endif = ParseTreeEdge(next_node=end, terminal="endif")
    endif_node = ParseTreeNode(next_edges=[endif])
    statement = ParseTreeEdge(next_node=endif_node, non_terminal="statement")
    statement_node = ParseTreeNode(next_edges=[statement])
    _else = ParseTreeEdge(next_node=statement_node, terminal="else")

    endif_2 = ParseTreeEdge(next_node=end, terminal="endif")

    return ParseTreeNode(next_edges=[_else, endif_2])


def selection_stmt_diagram():
    end = ParseTreeNode(next_edges=[])
    else_stmt = ParseTreeEdge(next_node=end, non_terminal="else_stmt")
    else_stmt_node = ParseTreeNode(next_edges=[else_stmt])
    statement = ParseTreeEdge(next_node=else_stmt_node, non_terminal="statement")
    statement_node = ParseTreeNode(next_edges=[statement])
    close_bracket = ParseTreeEdge(next_node=statement_node, terminal=")")
    close_bracket_node = ParseTreeNode(next_edges=[close_bracket])
    expression = ParseTreeEdge(next_node=close_bracket_node, non_terminal="expression")
    expression_node = ParseTreeNode(next_edges=[expression])
    open_bracket = ParseTreeEdge(next_node=expression_node, terminal="(")
    open_bracket_node = ParseTreeNode(next_edges=[open_bracket])
    _if = ParseTreeEdge(next_node=open_bracket_node, terminal="if")

    return ParseTreeNode(next_edges=[_if])


def expression_stmt_diagram():
    end = ParseTreeNode(next_edges=[])

    semicolon = ParseTreeEdge(next_node=end, terminal=";")

    semicolon_2 = ParseTreeEdge(next_node=end, terminal=";")
    semicolon_node = ParseTreeNode(next_edges=[semicolon_2])
    _break = ParseTreeEdge(next_node=semicolon_node, terminal="break")

    semicolon_3 = ParseTreeEdge(next_node=end, terminal=";")
    semicolon_node_2 = ParseTreeNode(next_edges=[semicolon_3])
    expression = ParseTreeEdge(next_node=semicolon_node_2, non_terminal="expression")

    return ParseTreeNode(next_edges=[semicolon, _break, expression])


def statement_diagram():
    end = ParseTreeNode(next_edges=[])

    expression_stmt = ParseTreeEdge(next_node=end, non_terminal="expression_stmt")

    compund_stmt = ParseTreeEdge(next_node=end, non_terminal="compund_stmt")

    selection_stmt = ParseTreeEdge(next_node=end, non_terminal="selection_stmt")

    iteration_stmt = ParseTreeEdge(next_node=end, non_terminal="iteration_stmt")

    return_stmt = ParseTreeEdge(next_node=end, non_terminal="statement_list")

    return ParseTreeNode(
        next_edges=[
            expression_stmt,
            compund_stmt,
            selection_stmt,
            iteration_stmt,
            return_stmt,
        ]
    )


def statement_list_diagram():
    end = ParseTreeNode(next_edges=[])
    statement_list = ParseTreeEdge(next_node=end, non_terminal="statement_list")
    statement_list_node = ParseTreeNode(next_edges=[statement_list])
    statement_bracket = ParseTreeEdge(
        next_node=statement_list_node, non_terminal="statement"
    )
    statement_node = ParseTreeNode(next_edges=[statement_bracket])

    epsilon_node = ParseTreeEdge(next_node=end, terminal="ε")

    return ParseTreeNode(next_edges=[statement_node, epsilon_node])


def compund_stmt():
    end = ParseTreeNode(next_edges=[])
    close_bracket = ParseTreeEdge(next_node=end, terminal="}")
    close_bracket_node = ParseTreeNode(next_edges=[close_bracket])
    statement_list = ParseTreeEdge(
        next_node=close_bracket_node, non_terminal="statement_list"
    )
    statement_list_node = ParseTreeNode(next_edges=[statement_list])
    declarion_list = ParseTreeEdge(
        next_node=statement_list_node, non_terminal="declarion_list"
    )
    declarion_list_node = ParseTreeNode(next_edges=[declarion_list])
    open_bracket = ParseTreeEdge(next_node=declarion_list_node, terminal="{")

    return ParseTreeNode(next_edges=[open_bracket])


def param_prime_diagram():
    end = ParseTreeNode(next_edges=[])
    close_bracket = ParseTreeEdge(next_node=end, terminal="]")
    close_bracket_node = ParseTreeNode(next_edges=[close_bracket])
    open_bracket = ParseTreeEdge(next_node=close_bracket_node, terminal="[")
    open_bracket_node = ParseTreeNode(next_edges=[open_bracket])

    epsilon_node = ParseTreeEdge(next_node=end, terminal="ε")

    return ParseTreeNode(next_edges=[open_bracket_node, epsilon_node])


def param_diagram():
    end = ParseTreeNode(next_edges=[])
    param_prime = ParseTreeEdge(next_node=end, non_terminal="param_prime")
    param_prime_node = ParseTreeNode(next_edges=[param_prime])

    return ParseTreeNode(next_edges=[param_prime_node])


def param_list_diagram():
    end = ParseTreeNode(next_edges=[])
    param_list = ParseTreeEdge(next_node=end, non_terminal="param_list")
    param_list_node = ParseTreeNode(next_edges=[param_list])
    param = ParseTreeEdge(next_node=param_list_node, non_terminal="param")
    param_node = ParseTreeNode(next_edges=[param])
    comma = ParseTreeEdge(next_node=param_node, terminal=",")

    epsilon_node = ParseTreeEdge(next_node=end, terminal="ε")

    return ParseTreeNode(next_edges=[comma, epsilon_node])


def params_diagram():
    end = ParseTreeNode(next_edges=[])
    param_list = ParseTreeEdge(next_node=end, non_terminal="param_list")
    param_list_node = ParseTreeNode(next_edges=[param_list])
    param_prime = ParseTreeEdge(next_node=param_list_node, non_terminal="param_prime")
    param_prime_node = ParseTreeNode(next_edges=[param_prime])
    _id = ParseTreeEdge(next_node=param_prime_node, terminal="ID")
    id_node = ParseTreeNode(next_edges=[_id])
    _int = ParseTreeEdge(next_node=id_node, terminal="int")

    _void = ParseTreeEdge(next_node=end, terminal="void")

    return ParseTreeNode(next_edges=[_int, _void])


def type_specifier_diagram():
    end = ParseTreeNode(next_edges=[])
    _int = ParseTreeEdge(next_node=end, terminal="int")

    _void = ParseTreeEdge(next_node=end, terminal="void")

    return ParseTreeNode(next_edges=[_int, _void])


def fun_declaration_prime():
    end = ParseTreeNode(next_edges=[])
    compound_stmt = ParseTreeEdge(next_node=end, non_terminal="compound_stmt")
    compound_stmt_node = ParseTreeNode(next_edges=[compound_stmt])
    close_par = ParseTreeEdge(next_node=compound_stmt_node, terminal=")")
    close_par_node = ParseTreeNode(next_edges=[close_par])
    params = ParseTreeEdge(next_node=close_par_node, non_terminal="params")
    params_node = ParseTreeNode(next_edges=[params])
    return ParseTreeEdge(next_node=params_node, terminal="(")


def var_declarion_prime_diagram():
    end = ParseTreeNode(next_edges=[])

    semicolon = ParseTreeEdge(next_node=end, terminal=";")

    semicolon_2 = ParseTreeEdge(next_node=end, terminal=";")
    semicolon_2_node = ParseTreeNode(next_edges=[semicolon_2])
    close_t = ParseTreeEdge(next_node=semicolon_2_node, terminal="]")
    num_node = ParseTreeNode(next_edges=[close_t])
    num = ParseTreeEdge(next_node=num_node, terminal="NUM")
    open_t_node = ParseTreeNode(next_edges=[num])
    open_t = ParseTreeEdge(next_node=open_t_node, terminal="[")

    return ParseTreeNode(next_edges=[semicolon, open_t])


def declaration_prime_diagram():
    end = ParseTreeNode(next_edges=[])
    fun_declartion_prime = ParseTreeEdge(
        next_node=end, non_terminal="fun_declartion_prime"
    )

    var_declartion_prime = ParseTreeEdge(
        next_node=end, non_terminal="var_declartion_prime"
    )

    return ParseTreeNode(next_edges=[fun_declartion_prime, var_declartion_prime])


def declaration_initial_diagram():
    end = ParseTreeNode(next_edges=[])
    _id = ParseTreeEdge(next_node=end, terminal="ID")
    id_node = ParseTreeNode(next_edges=[_id])
    type_specifier = ParseTreeEdge(next_node=id_node, non_terminal="type_specifier")
    return ParseTreeNode(next_edges=[type_specifier])


def declaration_diagram():
    end = ParseTreeNode(next_edges=[])
    declaration_prime = ParseTreeEdge(next_node=end, non_terminal="declaration_prime")
    declaration_prime_node = ParseTreeNode(next_edges=[declaration_prime])
    declaration_initial = ParseTreeEdge(
        next_node=declaration_prime_node, non_terminal="declaration_initial"
    )
    return ParseTreeNode(next_edges=[declaration_initial])


def declaration_list_diagram():
    end = ParseTreeNode(next_edges=[])
    declaration_list = ParseTreeEdge(next_node=end, non_terminal="declaration_list")
    declaration_list_node = ParseTreeNode(next_edges=[declaration_list])
    declaration = ParseTreeEdge(
        next_node=declaration_list_node, non_terminal="declaration"
    )

    epsilon_node = ParseTreeEdge(next_node=end, terminal="ε")

    return ParseTreeNode(next_edges=[declaration, epsilon_node])


def program_diagram():
    end = ParseTreeNode(next_edges=[])
    dollar = ParseTreeEdge(next_node=end, terminal="$")
    dollar_node = ParseTreeNode(next_edges=[dollar])
    declaration_list = ParseTreeEdge(
        next_node=dollar_node, non_terminal="declaration_list"
    )
    return ParseTreeNode(next_edges=[declaration_list])


def add_firsts():
    with open("firsts.txt", "r") as file:
        a = list(map(str.split, file.readlines()))
    for line in a:
        first_dict[str(line[0]).lower()] = line[1:]
