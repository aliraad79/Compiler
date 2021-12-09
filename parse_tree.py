from scanner import Token
from typing import List
from utils import format_non_terminal, return_firsts, return_follows


class IllegalToken(Exception):
    pass


class MissingToken(Exception):
    def __init__(self, next_node) -> None:
        self.next_node = next_node


def check_if_in_list(token: Token, list, epsilon=False):
    if epsilon:
        if token.type in ["ID", "NUM"]:
            return (token.type in list) or ("ε" in list)
        return (token.lexeme in list) or ("ε" in list)
    else:
        if token.type in ["ID", "NUM"]:
            return token.type in list
        elif token.type == "SYMBOL":
            return token.lexeme[0] in list
        else:
            return token.lexeme in list


class DiagramEdge:
    def __init__(
        self, next_node: "DiagramNode", terminal: str = None, non_terminal: str = None
    ):
        self.next_node = next_node
        self.terminal = terminal
        self.firsts: List[str] = None
        self.non_terminal = non_terminal

    def match(self, other: Token, stack: List[str], current_diagram_name):
        if self.non_terminal:
            if check_if_in_list(other, first_dict[self.non_terminal], epsilon=True):
                stack.append(self.non_terminal)
                return True

        elif self.terminal == "ε":
            return check_if_in_list(other, follows_dict[current_diagram_name])

        elif self.terminal:
            return other.lexeme == self.terminal or other.type == self.terminal

        return False

    def get_node_name(self):
        if self.non_terminal:
            return format_non_terminal(self.non_terminal)
        elif self.terminal == "ε":
            return "epsilon"
        elif self.terminal:
            return self.terminal

    def __repr__(self):
        return f"Edge<{self.terminal if self.terminal else self.non_terminal}>"


class DiagramNode:
    def __init__(self, next_edges: List[DiagramEdge] = []):
        self.next_edges = next_edges

    def next_diagram_tree_node(
        self,
        other: Token,
        stack: List[str],
        current_diagram_name: str,
    ):
        non_terminal_edge = None
        for i in self.next_edges:
            if i.non_terminal:
                non_terminal_edge: DiagramEdge = i
            if i.match(other, stack, current_diagram_name):
                return (
                    i.next_node,
                    (i.terminal != None and i.terminal != "ε" and i.terminal != "$"),
                    i.get_node_name(),
                )
        if len(self.next_edges) == 0:
            return None, False, None

        # Errors
        follows = follows_dict[
            non_terminal_edge.non_terminal
            if non_terminal_edge.non_terminal
            else current_diagram_name
        ]
        if (other.lexeme not in follows) and (other.type not in follows):
            raise IllegalToken()
        else:
            raise MissingToken(non_terminal_edge.next_node)

    def __repr__(self):
        return f"Node<next_edges = {self.next_edges}>"


first_dict = return_firsts()
follows_dict = return_follows()


def get_transation_diagrams():
    return {
        "program": program_diagram(),
        "declaration_list": declaration_list_diagram(),
        "declaration": declaration_diagram(),
        "declaration_initial": declaration_initial_diagram(),
        "declaration_prime": declaration_prime_diagram(),
        "var_declaration_prime": var_declaration_prime_diagram(),
        "fun_declaration_prime": fun_declaration_prime(),
        "type_specifier": type_specifier_diagram(),
        "params": params_diagram(),
        "param_list": param_list_diagram(),
        "param": param_diagram(),
        "param_prime": param_prime_diagram(),
        "compound_stmt": compound_stmt(),
        "statement_list": statement_list_diagram(),
        "statement": statement_diagram(),
        "expression_stmt": expression_stmt_diagram(),
        "selection_stmt": selection_stmt_diagram(),
        "else_stmt": else_stmt_diagram(),
        "iteration_stmt": iteration_stmt_diagram(),
        "return_stmt": return_stmt_diagram(),
        "return_stmt_prime": return_stmt_prime_diagram(),
        "expression": expression_diagram(),
        "b": B_diagram(),
        "h": H_diagram(),
        "simple_expression_zegond": simple_expression_zegond_diagram(),
        "simple_expression_prime": simple_expression_prime_diagram(),
        "c": C_diagram(),
        "relop": relop_diagram(),
        "additive_expression": additive_expression_diagram(),
        "additive_expression_prime": additive_expression_prime_diagram(),
        "additive_expression_zegond": additive_expression_zegond_diagram(),
        "d": D_diagram(),
        "addop": addop_diagram(),
        "term": term_diagram(),
        "term_prime": term_prime_diagram(),
        "term_zegond": term_zegond_diagram(),
        "g": G_diagram(),
        "factor": factor_diagram(),
        "var_call_prime": var_call_prime_diagram(),
        "var_prime": var_prime_diagram(),
        "factor_prime": factor_prime_diagram(),
        "factor_zegond": factor_zegond_diagram(),
        "args": args_diagram(),
        "arg_list": arg_list_diagram(),
        "arg_list_prime": arg_list_prime_diagram(),
    }


def arg_list_prime_diagram():
    end = DiagramNode(next_edges=[])
    arg_list_prime = DiagramEdge(next_node=end, non_terminal="arg_list_prime")
    arg_list_prime_node = DiagramNode(next_edges=[arg_list_prime])
    expression = DiagramEdge(next_node=arg_list_prime_node, non_terminal="expression")
    expression_node = DiagramNode(next_edges=[expression])
    comma = DiagramEdge(next_node=expression_node, terminal=",")

    epsilon_node = DiagramEdge(next_node=end, terminal="ε")

    return DiagramNode(next_edges=[comma, epsilon_node])


def arg_list_diagram():
    end = DiagramNode(next_edges=[])
    arg_list_prime = DiagramEdge(next_node=end, non_terminal="arg_list_prime")
    arg_list_prime_node = DiagramNode(next_edges=[arg_list_prime])
    expression = DiagramEdge(next_node=arg_list_prime_node, non_terminal="expression")

    return DiagramNode(next_edges=[expression])


def args_diagram():
    end = DiagramNode(next_edges=[])
    arg_list = DiagramEdge(next_node=end, non_terminal="arg_list")

    epsilon_node = DiagramEdge(next_node=end, terminal="ε")

    return DiagramNode(next_edges=[arg_list, epsilon_node])


def factor_zegond_diagram():
    end = DiagramNode(next_edges=[])
    close_par = DiagramEdge(next_node=end, terminal=")")
    close_par_node = DiagramNode(next_edges=[close_par])
    expression = DiagramEdge(next_node=close_par_node, non_terminal="expression")
    expression_node = DiagramNode(next_edges=[expression])
    open_par = DiagramEdge(next_node=expression_node, terminal="(")

    num = DiagramEdge(next_node=end, terminal="NUM")

    return DiagramNode(next_edges=[open_par, num])


def factor_prime_diagram():
    end = DiagramNode(next_edges=[])
    close_par = DiagramEdge(next_node=end, terminal=")")
    close_par_node = DiagramNode(next_edges=[close_par])
    args = DiagramEdge(next_node=close_par_node, non_terminal="args")
    args_node = DiagramNode(next_edges=[args])
    open_par = DiagramEdge(next_node=args_node, terminal="(")

    epsilon_node = DiagramEdge(next_node=end, terminal="ε")

    return DiagramNode(next_edges=[open_par, epsilon_node])


def var_prime_diagram():
    end = DiagramNode(next_edges=[])
    close_par = DiagramEdge(next_node=end, terminal="]")
    close_par_node = DiagramNode(next_edges=[close_par])
    expression = DiagramEdge(next_node=close_par_node, non_terminal="expression")
    expression_node = DiagramNode(next_edges=[expression])
    open_par = DiagramEdge(next_node=expression_node, terminal="[")

    epsilon_node = DiagramEdge(next_node=end, terminal="ε")

    return DiagramNode(next_edges=[open_par, epsilon_node])


def var_call_prime_diagram():
    end = DiagramNode(next_edges=[])
    close_par = DiagramEdge(next_node=end, terminal=")")
    close_par_node = DiagramNode(next_edges=[close_par])
    args = DiagramEdge(next_node=close_par_node, non_terminal="args")
    args_node = DiagramNode(next_edges=[args])
    open_par = DiagramEdge(next_node=args_node, terminal="(")

    var_prime = DiagramEdge(next_node=end, non_terminal="var_prime")

    return DiagramNode(next_edges=[open_par, var_prime])


def factor_diagram():
    end = DiagramNode(next_edges=[])
    close_par = DiagramEdge(next_node=end, terminal=")")
    close_par_node = DiagramNode(next_edges=[close_par])
    expression = DiagramEdge(next_node=close_par_node, non_terminal="expression")
    expression_node = DiagramNode(next_edges=[expression])
    open_par = DiagramEdge(next_node=expression_node, terminal="(")

    var_call_prime = DiagramEdge(next_node=end, non_terminal="var_call_prime")
    var_call_prime_node = DiagramNode(next_edges=[var_call_prime])
    _id = DiagramEdge(next_node=var_call_prime_node, terminal="ID")

    num = DiagramEdge(next_node=end, terminal="NUM")

    return DiagramNode(next_edges=[open_par, num, _id])


def G_diagram():
    end = DiagramNode(next_edges=[])
    _G_edge = DiagramEdge(next_node=end, non_terminal="g")
    _G_node = DiagramNode(next_edges=[_G_edge])
    factor = DiagramEdge(next_node=_G_node, non_terminal="factor")
    factor_node = DiagramNode(next_edges=[factor])
    star = DiagramEdge(next_node=factor_node, terminal="*")

    epsilon_node = DiagramEdge(next_node=end, terminal="ε")

    return DiagramNode(next_edges=[star, epsilon_node])


def term_zegond_diagram():
    end = DiagramNode(next_edges=[])
    _G_edge = DiagramEdge(next_node=end, non_terminal="g")
    _G_node = DiagramNode(next_edges=[_G_edge])
    factor_zegond = DiagramEdge(next_node=_G_node, non_terminal="factor_zegond")

    return DiagramNode(next_edges=[factor_zegond])


def term_prime_diagram():
    end = DiagramNode(next_edges=[])
    _G_edge = DiagramEdge(next_node=end, non_terminal="g")
    _G_node = DiagramNode(next_edges=[_G_edge])
    factor_prime = DiagramEdge(next_node=_G_node, non_terminal="factor_prime")

    return DiagramNode(next_edges=[factor_prime])


def term_diagram():
    end = DiagramNode(next_edges=[])
    _G_edge = DiagramEdge(next_node=end, non_terminal="g")
    _G_node = DiagramNode(next_edges=[_G_edge])
    factor = DiagramEdge(next_node=_G_node, non_terminal="factor")

    return DiagramNode(next_edges=[factor])


def addop_diagram():
    end = DiagramNode(next_edges=[])
    plus = DiagramEdge(next_node=end, terminal="+")

    minus = DiagramEdge(next_node=end, terminal="-")

    return DiagramNode(next_edges=[plus, minus])


def D_diagram():
    end = DiagramNode(next_edges=[])
    _D_edge = DiagramEdge(next_node=end, non_terminal="d")
    _D_node = DiagramNode(next_edges=[_D_edge])
    term = DiagramEdge(next_node=_D_node, non_terminal="term")
    term_node = DiagramNode(next_edges=[term])
    addop = DiagramEdge(next_node=term_node, non_terminal="addop")

    epsilon_node = DiagramEdge(next_node=end, terminal="ε")

    return DiagramNode(next_edges=[addop, epsilon_node])


def additive_expression_zegond_diagram():
    end = DiagramNode(next_edges=[])
    _D_edge = DiagramEdge(next_node=end, non_terminal="d")
    _D_node = DiagramNode(next_edges=[_D_edge])
    term_zegond = DiagramEdge(next_node=_D_node, non_terminal="term_zegond")

    return DiagramNode(next_edges=[term_zegond])


def additive_expression_prime_diagram():
    end = DiagramNode(next_edges=[])
    _D_edge = DiagramEdge(next_node=end, non_terminal="d")
    _D_node = DiagramNode(next_edges=[_D_edge])
    term_prime = DiagramEdge(next_node=_D_node, non_terminal="term_prime")

    return DiagramNode(next_edges=[term_prime])


def additive_expression_diagram():
    end = DiagramNode(next_edges=[])
    _D_edge = DiagramEdge(next_node=end, non_terminal="d")
    _D_node = DiagramNode(next_edges=[_D_edge])
    term = DiagramEdge(next_node=_D_node, non_terminal="term")

    return DiagramNode(next_edges=[term])


def relop_diagram():
    end = DiagramNode(next_edges=[])
    lower = DiagramEdge(next_node=end, terminal="<")

    equal_1 = DiagramEdge(next_node=end, terminal="=")
    equal_1_node = DiagramNode(next_edges=[equal_1])
    equal_2 = DiagramEdge(next_node=equal_1_node, terminal="=")

    return DiagramNode(next_edges=[lower, equal_2])


def C_diagram():
    end = DiagramNode(next_edges=[])
    additive_expression = DiagramEdge(next_node=end, non_terminal="additive_expression")
    additive_expression_node = DiagramNode(next_edges=[additive_expression])
    relop = DiagramEdge(next_node=additive_expression_node, non_terminal="relop")

    epsilon_node = DiagramEdge(next_node=end, terminal="ε")

    return DiagramNode(next_edges=[relop, epsilon_node])


def simple_expression_prime_diagram():
    end = DiagramNode(next_edges=[])
    _C_edge = DiagramEdge(next_node=end, non_terminal="c")
    _C_node = DiagramNode(next_edges=[_C_edge])
    additive_expression_prime = DiagramEdge(
        next_node=_C_node, non_terminal="additive_expression_prime"
    )

    return DiagramNode(next_edges=[additive_expression_prime])


def simple_expression_zegond_diagram():
    end = DiagramNode(next_edges=[])
    _C_edge = DiagramEdge(next_node=end, non_terminal="c")
    _C_node = DiagramNode(next_edges=[_C_edge])
    additive_expression_zegond = DiagramEdge(
        next_node=_C_node, non_terminal="additive_expression_zegond"
    )

    return DiagramNode(next_edges=[additive_expression_zegond])


def H_diagram():
    end = DiagramNode(next_edges=[])
    _C_edge = DiagramEdge(next_node=end, non_terminal="c")
    _C_node = DiagramNode(next_edges=[_C_edge])
    _D_edge = DiagramEdge(next_node=_C_node, non_terminal="d")
    _D_node = DiagramNode(next_edges=[_D_edge])
    _G_edge = DiagramEdge(next_node=_D_node, non_terminal="g")

    expression = DiagramEdge(next_node=end, non_terminal="expression")

    return DiagramNode(next_edges=[expression, _G_edge])


def B_diagram():
    end = DiagramNode(next_edges=[])

    _H_edge = DiagramEdge(next_node=end, non_terminal="h")
    _H_node = DiagramNode(next_edges=[_H_edge])
    close_par = DiagramEdge(next_node=_H_node, terminal="]")
    close_par_node = DiagramNode(next_edges=[close_par])
    expression = DiagramEdge(next_node=close_par_node, non_terminal="expression")
    expression_node = DiagramNode(next_edges=[expression])
    open_par = DiagramEdge(next_node=expression_node, terminal="[")

    expression_2 = DiagramEdge(next_node=end, non_terminal="expression")
    expression_2_node = DiagramNode(next_edges=[expression_2])
    equal = DiagramEdge(next_node=expression_2_node, terminal="=")

    simple_expression_prime = DiagramEdge(
        next_node=end, non_terminal="simple_expression_prime"
    )

    return DiagramNode(next_edges=[open_par, equal, simple_expression_prime])


def expression_diagram():
    end = DiagramNode(next_edges=[])
    _B_edge = DiagramEdge(next_node=end, non_terminal="b")
    _B_node = DiagramNode(next_edges=[_B_edge])
    _id = DiagramEdge(next_node=_B_node, terminal="ID")

    simple_expression_zegond = DiagramEdge(
        next_node=end, non_terminal="simple_expression_zegond"
    )

    return DiagramNode(next_edges=[simple_expression_zegond, _id])


def return_stmt_prime_diagram():
    end = DiagramNode(next_edges=[])

    semicolon_2 = DiagramEdge(next_node=end, terminal=";")
    semicolon_2_node = DiagramNode(next_edges=[semicolon_2])
    expression = DiagramEdge(next_node=semicolon_2_node, non_terminal="expression")

    semicolon = DiagramEdge(next_node=end, terminal=";")

    return DiagramNode(next_edges=[semicolon, expression])


def return_stmt_diagram():
    end = DiagramNode(next_edges=[])
    return_stmt_prime = DiagramEdge(next_node=end, non_terminal="return_stmt_prime")
    statement_node = DiagramNode(next_edges=[return_stmt_prime])
    _return = DiagramEdge(next_node=statement_node, terminal="return")

    return DiagramNode(next_edges=[_return])


def iteration_stmt_diagram():
    end = DiagramNode(next_edges=[])
    close_bracket = DiagramEdge(next_node=end, terminal=")")
    close_bracket_node = DiagramNode(next_edges=[close_bracket])
    expression = DiagramEdge(next_node=close_bracket_node, non_terminal="expression")
    expression_node = DiagramNode(next_edges=[expression])
    open_bracket = DiagramEdge(next_node=expression_node, terminal="(")
    open_bracket_node = DiagramNode(next_edges=[open_bracket])
    until = DiagramEdge(next_node=open_bracket_node, terminal="until")
    until_node = DiagramNode(next_edges=[until])
    statement = DiagramEdge(next_node=until_node, non_terminal="statement")
    statement_node = DiagramNode(next_edges=[statement])
    repeat = DiagramEdge(next_node=statement_node, terminal="repeat")

    return DiagramNode(next_edges=[repeat])


def else_stmt_diagram():
    end = DiagramNode(next_edges=[])
    endif = DiagramEdge(next_node=end, terminal="endif")
    endif_node = DiagramNode(next_edges=[endif])
    statement = DiagramEdge(next_node=endif_node, non_terminal="statement")
    statement_node = DiagramNode(next_edges=[statement])
    _else = DiagramEdge(next_node=statement_node, terminal="else")

    endif_2 = DiagramEdge(next_node=end, terminal="endif")

    return DiagramNode(next_edges=[_else, endif_2])


def selection_stmt_diagram():
    end = DiagramNode(next_edges=[])
    else_stmt = DiagramEdge(next_node=end, non_terminal="else_stmt")
    else_stmt_node = DiagramNode(next_edges=[else_stmt])
    statement = DiagramEdge(next_node=else_stmt_node, non_terminal="statement")
    statement_node = DiagramNode(next_edges=[statement])
    close_bracket = DiagramEdge(next_node=statement_node, terminal=")")
    close_bracket_node = DiagramNode(next_edges=[close_bracket])
    expression = DiagramEdge(next_node=close_bracket_node, non_terminal="expression")
    expression_node = DiagramNode(next_edges=[expression])
    open_bracket = DiagramEdge(next_node=expression_node, terminal="(")
    open_bracket_node = DiagramNode(next_edges=[open_bracket])
    _if = DiagramEdge(next_node=open_bracket_node, terminal="if")

    return DiagramNode(next_edges=[_if])


def expression_stmt_diagram():
    end = DiagramNode(next_edges=[])

    semicolon = DiagramEdge(next_node=end, terminal=";")

    semicolon_2 = DiagramEdge(next_node=end, terminal=";")
    semicolon_node = DiagramNode(next_edges=[semicolon_2])
    _break = DiagramEdge(next_node=semicolon_node, terminal="break")

    semicolon_3 = DiagramEdge(next_node=end, terminal=";")
    semicolon_node_2 = DiagramNode(next_edges=[semicolon_3])
    expression = DiagramEdge(next_node=semicolon_node_2, non_terminal="expression")

    return DiagramNode(next_edges=[semicolon, _break, expression])


def statement_diagram():
    end = DiagramNode(next_edges=[])

    expression_stmt = DiagramEdge(next_node=end, non_terminal="expression_stmt")

    compound_stmt = DiagramEdge(next_node=end, non_terminal="compound_stmt")

    selection_stmt = DiagramEdge(next_node=end, non_terminal="selection_stmt")

    iteration_stmt = DiagramEdge(next_node=end, non_terminal="iteration_stmt")

    return_stmt = DiagramEdge(next_node=end, non_terminal="return_stmt")

    return DiagramNode(
        next_edges=[
            expression_stmt,
            compound_stmt,
            selection_stmt,
            iteration_stmt,
            return_stmt,
        ]
    )


def statement_list_diagram():
    end = DiagramNode(next_edges=[])
    statement_list = DiagramEdge(next_node=end, non_terminal="statement_list")
    statement_list_node = DiagramNode(next_edges=[statement_list])
    statement = DiagramEdge(next_node=statement_list_node, non_terminal="statement")

    epsilon_node = DiagramEdge(next_node=end, terminal="ε")

    return DiagramNode(next_edges=[statement, epsilon_node])


def compound_stmt():
    end = DiagramNode(next_edges=[])
    close_bracket = DiagramEdge(next_node=end, terminal="}")
    close_bracket_node = DiagramNode(next_edges=[close_bracket])
    statement_list = DiagramEdge(
        next_node=close_bracket_node, non_terminal="statement_list"
    )
    statement_list_node = DiagramNode(next_edges=[statement_list])
    declaration_list = DiagramEdge(
        next_node=statement_list_node, non_terminal="declaration_list"
    )
    declaration_list_node = DiagramNode(next_edges=[declaration_list])
    open_bracket = DiagramEdge(next_node=declaration_list_node, terminal="{")

    return DiagramNode(next_edges=[open_bracket])


def param_prime_diagram():
    end = DiagramNode(next_edges=[])
    close_bracket = DiagramEdge(next_node=end, terminal="]")
    close_bracket_node = DiagramNode(next_edges=[close_bracket])
    open_bracket = DiagramEdge(next_node=close_bracket_node, terminal="[")

    epsilon_node = DiagramEdge(next_node=end, terminal="ε")

    return DiagramNode(next_edges=[open_bracket, epsilon_node])


def param_diagram():
    end = DiagramNode(next_edges=[])
    param_prime = DiagramEdge(next_node=end, non_terminal="param_prime")
    param_prime_node = DiagramNode(next_edges=[param_prime])

    return DiagramNode(next_edges=[param_prime_node])


def param_list_diagram():
    end = DiagramNode(next_edges=[])
    param_list = DiagramEdge(next_node=end, non_terminal="param_list")
    param_list_node = DiagramNode(next_edges=[param_list])
    param = DiagramEdge(next_node=param_list_node, non_terminal="param")
    param_node = DiagramNode(next_edges=[param])
    comma = DiagramEdge(next_node=param_node, terminal=",")

    epsilon_node = DiagramEdge(next_node=end, terminal="ε")

    return DiagramNode(next_edges=[comma, epsilon_node])


def params_diagram():
    end = DiagramNode(next_edges=[])
    param_list = DiagramEdge(next_node=end, non_terminal="param_list")
    param_list_node = DiagramNode(next_edges=[param_list])
    param_prime = DiagramEdge(next_node=param_list_node, non_terminal="param_prime")
    param_prime_node = DiagramNode(next_edges=[param_prime])
    _id = DiagramEdge(next_node=param_prime_node, terminal="ID")
    id_node = DiagramNode(next_edges=[_id])
    _int = DiagramEdge(next_node=id_node, terminal="int")

    _void = DiagramEdge(next_node=end, terminal="void")

    return DiagramNode(next_edges=[_int, _void])


def type_specifier_diagram():
    end = DiagramNode(next_edges=[])
    _int = DiagramEdge(next_node=end, terminal="int")

    _void = DiagramEdge(next_node=end, terminal="void")

    return DiagramNode(next_edges=[_int, _void])


def fun_declaration_prime():
    end = DiagramNode(next_edges=[])
    compound_stmt = DiagramEdge(next_node=end, non_terminal="compound_stmt")
    compound_stmt_node = DiagramNode(next_edges=[compound_stmt])
    close_par = DiagramEdge(next_node=compound_stmt_node, terminal=")")
    close_par_node = DiagramNode(next_edges=[close_par])
    params = DiagramEdge(next_node=close_par_node, non_terminal="params")
    params_node = DiagramNode(next_edges=[params])
    open_par = DiagramEdge(next_node=params_node, terminal="(")
    return DiagramNode(next_edges=[open_par])


def var_declaration_prime_diagram():
    end = DiagramNode(next_edges=[])

    semicolon = DiagramEdge(next_node=end, terminal=";")

    semicolon_2 = DiagramEdge(next_node=end, terminal=";")
    semicolon_2_node = DiagramNode(next_edges=[semicolon_2])
    close_t = DiagramEdge(next_node=semicolon_2_node, terminal="]")
    num_node = DiagramNode(next_edges=[close_t])
    num = DiagramEdge(next_node=num_node, terminal="NUM")
    open_t_node = DiagramNode(next_edges=[num])
    open_t = DiagramEdge(next_node=open_t_node, terminal="[")

    return DiagramNode(next_edges=[semicolon, open_t])


def declaration_prime_diagram():
    end = DiagramNode(next_edges=[])
    fun_declaration_prime = DiagramEdge(
        next_node=end, non_terminal="fun_declaration_prime"
    )

    var_declaration_prime = DiagramEdge(
        next_node=end, non_terminal="var_declaration_prime"
    )

    return DiagramNode(next_edges=[fun_declaration_prime, var_declaration_prime])


def declaration_initial_diagram():
    end = DiagramNode(next_edges=[])
    _id = DiagramEdge(next_node=end, terminal="ID")
    id_node = DiagramNode(next_edges=[_id])
    type_specifier = DiagramEdge(next_node=id_node, non_terminal="type_specifier")
    return DiagramNode(next_edges=[type_specifier])


def declaration_diagram():
    end = DiagramNode(next_edges=[])
    declaration_prime = DiagramEdge(next_node=end, non_terminal="declaration_prime")
    declaration_prime_node = DiagramNode(next_edges=[declaration_prime])
    declaration_initial = DiagramEdge(
        next_node=declaration_prime_node, non_terminal="declaration_initial"
    )
    return DiagramNode(next_edges=[declaration_initial])


def declaration_list_diagram():
    end = DiagramNode(next_edges=[])
    declaration_list = DiagramEdge(next_node=end, non_terminal="declaration_list")
    declaration_list_node = DiagramNode(next_edges=[declaration_list])
    declaration = DiagramEdge(
        next_node=declaration_list_node, non_terminal="declaration"
    )

    epsilon_node = DiagramEdge(next_node=end, terminal="ε")

    return DiagramNode(next_edges=[declaration, epsilon_node])


def program_diagram():
    end = DiagramNode(next_edges=[])
    dollar = DiagramEdge(next_node=end, terminal="$")
    dollar_node = DiagramNode(next_edges=[dollar])
    declaration_list = DiagramEdge(
        next_node=dollar_node, non_terminal="declaration_list"
    )
    return DiagramNode(next_edges=[declaration_list])
