from scanner import Token
from typing import List
from utils import format_non_terminal, return_firsts, return_follows


class IllegalToken(Exception):
    pass


class MissingToken(Exception):
    def __init__(self, next_edge: "DiagramEdge") -> None:
        self.next_edge = next_edge


def check_token_in_list(token: Token, target_list, include_epsilon=False):
    return (
        True
        if include_epsilon and "ε" in target_list
        else token.parse_name in target_list
    )


class DiagramEdge:
    def __init__(
        self,
        next_node: "DiagramNode",
        terminal: str = None,
        non_terminal: str = None,
        action_symbols: List[str] = None,
    ):
        self.next_node = next_node
        self.terminal = terminal
        self.firsts: List[str] = None
        self.non_terminal = non_terminal
        self.action_symbols = action_symbols

    def match(self, other: Token, current_diagram_name):
        """
        Can match token to link
        """

        if self.non_terminal:
            return check_token_in_list(
                other, first_dict[self.non_terminal], include_epsilon=True
            )

        elif self.terminal == "ε":
            return check_token_in_list(other, follows_dict[current_diagram_name])

        elif self.terminal:
            return other.lexeme == self.terminal or other.type == self.terminal

        return False

    @property
    def parse_tree_name(self):
        if self.non_terminal:
            return format_non_terminal(self.non_terminal)
        return "epsilon" if self.terminal == "ε" else self.terminal

    def __repr__(self):
        return f"Edge<{self.terminal if self.terminal else self.non_terminal}>"


class DiagramNode:
    def __init__(self, next_edges: List[DiagramEdge] = [], is_first: bool = False):
        self.next_edges = next_edges
        self.is_first = is_first
        # self.action_symbol =

    def next_diagram_tree_node(self, other: Token, current_diagram_name: str):

        # save terminal and non terminal edges for error handling
        non_terminal_edge = None
        terminal_edge = None

        # loop through edges
        for i in self.next_edges:
            # set terminal and non-terminal edges for further error handling
            if i.non_terminal:
                non_terminal_edge: DiagramEdge = i
            elif i.terminal and i.terminal != "ε":
                terminal_edge: DiagramEdge = i

            if i.match(other, current_diagram_name):
                is_pure_terminal = (
                    i.terminal != None and i.terminal != "ε" and i.terminal != "$"
                )
                return_node_name = i.non_terminal if i.non_terminal else None
                return i, is_pure_terminal, return_node_name
        # End of diagram
        if len(self.next_edges) == 0:
            return None, False, None

        # Errors
        # miss the terminal at the beginning of diagram
        if terminal_edge and not self.is_first:
            raise MissingToken(terminal_edge)

        follows = follows_dict[
            non_terminal_edge.non_terminal
            if non_terminal_edge and non_terminal_edge.non_terminal
            else current_diagram_name
        ]
        # if in follows
        if check_token_in_list(other, follows):
            raise MissingToken(
                non_terminal_edge if non_terminal_edge else self.next_edges[0]
            )
        else:
            raise IllegalToken()

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
    arg_list_prime = DiagramEdge(next_node=end, non_terminal="arg_list_prime", action_symbols=["assign_arg"])
    arg_list_prime_node = DiagramNode(next_edges=[arg_list_prime])
    expression = DiagramEdge(next_node=arg_list_prime_node, non_terminal="expression", action_symbols=['push_arg'])
    expression_node = DiagramNode(next_edges=[expression])
    comma = DiagramEdge(next_node=expression_node, terminal=",")

    epsilon_node = DiagramEdge(next_node=end, terminal="ε")

    return DiagramNode(next_edges=[comma, epsilon_node], is_first=True)


def arg_list_diagram():
    end = DiagramNode(next_edges=[])
    arg_list_prime = DiagramEdge(
        next_node=end, non_terminal="arg_list_prime", action_symbols=["assign_arg"]
    )
    arg_list_prime_node = DiagramNode(next_edges=[arg_list_prime])
    expression = DiagramEdge(
        next_node=arg_list_prime_node,
        non_terminal="expression",
        action_symbols=["push_arg"],
    )

    return DiagramNode(next_edges=[expression], is_first=True)


def args_diagram():
    end = DiagramNode(next_edges=[])
    arg_list = DiagramEdge(next_node=end, non_terminal="arg_list")

    epsilon_node = DiagramEdge(next_node=end, terminal="ε")

    return DiagramNode(next_edges=[arg_list, epsilon_node], is_first=True)


def factor_zegond_diagram():
    end = DiagramNode(next_edges=[])
    close_par = DiagramEdge(next_node=end, terminal=")")
    close_par_node = DiagramNode(next_edges=[close_par])
    expression = DiagramEdge(next_node=close_par_node, non_terminal="expression")
    expression_node = DiagramNode(next_edges=[expression])
    open_par = DiagramEdge(next_node=expression_node, terminal="(")

    num = DiagramEdge(next_node=end, terminal="NUM", action_symbols=["padd"])

    return DiagramNode(next_edges=[open_par, num], is_first=True)


def factor_prime_diagram():
    end = DiagramNode(next_edges=[])
    close_par = DiagramEdge(
        next_node=end, terminal=")", action_symbols=["func_call_ended"]
    )
    close_par_node = DiagramNode(next_edges=[close_par])
    args = DiagramEdge(next_node=close_par_node, non_terminal="args")
    args_node = DiagramNode(next_edges=[args])
    open_par = DiagramEdge(
        next_node=args_node, terminal="(", action_symbols=["func_call_started"]
    )

    epsilon_node = DiagramEdge(next_node=end, terminal="ε")

    return DiagramNode(next_edges=[open_par, epsilon_node], is_first=True)


def var_prime_diagram():
    end = DiagramNode(next_edges=[])
    close_par = DiagramEdge(
        next_node=end, terminal="]", action_symbols=["set_array_address"]
    )
    close_par_node = DiagramNode(next_edges=[close_par])
    expression = DiagramEdge(next_node=close_par_node, non_terminal="expression")
    expression_node = DiagramNode(next_edges=[expression])
    open_par = DiagramEdge(next_node=expression_node, terminal="[")

    epsilon_node = DiagramEdge(next_node=end, terminal="ε")

    return DiagramNode(next_edges=[open_par, epsilon_node], is_first=True)


def var_call_prime_diagram():
    end = DiagramNode(next_edges=[])
    close_par = DiagramEdge(
        next_node=end, terminal=")", action_symbols=["func_call_ended"]
    )
    close_par_node = DiagramNode(next_edges=[close_par])
    args = DiagramEdge(next_node=close_par_node, non_terminal="args")
    args_node = DiagramNode(next_edges=[args])
    open_par = DiagramEdge(
        next_node=args_node, terminal="(", action_symbols=["func_call_started"]
    )

    var_prime = DiagramEdge(next_node=end, non_terminal="var_prime")

    return DiagramNode(next_edges=[open_par, var_prime], is_first=True)


def factor_diagram():
    end = DiagramNode(next_edges=[])
    close_par = DiagramEdge(next_node=end, terminal=")")
    close_par_node = DiagramNode(next_edges=[close_par])
    expression = DiagramEdge(next_node=close_par_node, non_terminal="expression")
    expression_node = DiagramNode(next_edges=[expression])
    open_par = DiagramEdge(next_node=expression_node, terminal="(")

    var_call_prime = DiagramEdge(next_node=end, non_terminal="var_call_prime")
    var_call_prime_node = DiagramNode(next_edges=[var_call_prime])
    _id = DiagramEdge(
        next_node=var_call_prime_node, terminal="ID", action_symbols=["padd"]
    )

    num = DiagramEdge(next_node=end, terminal="NUM", action_symbols=["padd"])

    return DiagramNode(next_edges=[open_par, num, _id], is_first=True)


def G_diagram():
    end = DiagramNode(next_edges=[])
    _G_edge = DiagramEdge(next_node=end, non_terminal="g", action_symbols=["op"])
    _G_node = DiagramNode(next_edges=[_G_edge])
    factor = DiagramEdge(next_node=_G_node, non_terminal="factor")
    factor_node = DiagramNode(next_edges=[factor])
    star = DiagramEdge(next_node=factor_node, terminal="*", action_symbols=["padd"])

    epsilon_node = DiagramEdge(next_node=end, terminal="ε")

    return DiagramNode(next_edges=[star, epsilon_node], is_first=True)


def term_zegond_diagram():
    end = DiagramNode(next_edges=[])
    _G_edge = DiagramEdge(next_node=end, non_terminal="g")
    _G_node = DiagramNode(next_edges=[_G_edge])
    factor_zegond = DiagramEdge(next_node=_G_node, non_terminal="factor_zegond")

    return DiagramNode(next_edges=[factor_zegond], is_first=True)


def term_prime_diagram():
    end = DiagramNode(next_edges=[])
    _G_edge = DiagramEdge(next_node=end, non_terminal="g")
    _G_node = DiagramNode(next_edges=[_G_edge])
    factor_prime = DiagramEdge(next_node=_G_node, non_terminal="factor_prime")

    return DiagramNode(next_edges=[factor_prime], is_first=True)


def term_diagram():
    end = DiagramNode(next_edges=[])
    _G_edge = DiagramEdge(next_node=end, non_terminal="g")
    _G_node = DiagramNode(next_edges=[_G_edge])
    factor = DiagramEdge(next_node=_G_node, non_terminal="factor")

    return DiagramNode(next_edges=[factor], is_first=True)


def addop_diagram():
    end = DiagramNode(next_edges=[])
    plus = DiagramEdge(next_node=end, terminal="+")

    minus = DiagramEdge(next_node=end, terminal="-")

    return DiagramNode(next_edges=[plus, minus], is_first=True)


def D_diagram():
    end = DiagramNode(next_edges=[])
    _D_edge = DiagramEdge(next_node=end, non_terminal="d", action_symbols=["op"])
    _D_node = DiagramNode(next_edges=[_D_edge])
    term = DiagramEdge(next_node=_D_node, non_terminal="term")
    term_node = DiagramNode(next_edges=[term])
    addop = DiagramEdge(
        next_node=term_node, non_terminal="addop", action_symbols=["padd"]
    )

    epsilon_node = DiagramEdge(next_node=end, terminal="ε")

    return DiagramNode(next_edges=[addop, epsilon_node], is_first=True)


def additive_expression_zegond_diagram():
    end = DiagramNode(next_edges=[])
    _D_edge = DiagramEdge(next_node=end, non_terminal="d")
    _D_node = DiagramNode(next_edges=[_D_edge])
    term_zegond = DiagramEdge(next_node=_D_node, non_terminal="term_zegond")

    return DiagramNode(next_edges=[term_zegond], is_first=True)


def additive_expression_prime_diagram():
    end = DiagramNode(next_edges=[])
    _D_edge = DiagramEdge(next_node=end, non_terminal="d")
    _D_node = DiagramNode(next_edges=[_D_edge])
    term_prime = DiagramEdge(next_node=_D_node, non_terminal="term_prime")

    return DiagramNode(next_edges=[term_prime], is_first=True)


def additive_expression_diagram():
    end = DiagramNode(next_edges=[])
    _D_edge = DiagramEdge(next_node=end, non_terminal="d")
    _D_node = DiagramNode(next_edges=[_D_edge])
    term = DiagramEdge(next_node=_D_node, non_terminal="term")

    return DiagramNode(next_edges=[term], is_first=True)


def relop_diagram():
    end = DiagramNode(next_edges=[])
    lower = DiagramEdge(next_node=end, terminal="<")

    equal_2 = DiagramEdge(next_node=end, terminal="==")

    return DiagramNode(next_edges=[lower, equal_2], is_first=True)


def C_diagram():
    end = DiagramNode(next_edges=[])

    dummy_edge = DiagramEdge(next_node=end, terminal="ε", action_symbols=["op"])
    dummy_node = DiagramNode(next_edges=[dummy_edge])
    additive_expression = DiagramEdge(
        next_node=dummy_node, non_terminal="additive_expression"
    )
    additive_expression_node = DiagramNode(next_edges=[additive_expression])
    relop = DiagramEdge(
        next_node=additive_expression_node,
        non_terminal="relop",
        action_symbols=["padd"],
    )

    epsilon_node = DiagramEdge(next_node=end, terminal="ε")

    return DiagramNode(next_edges=[relop, epsilon_node], is_first=True)


def simple_expression_prime_diagram():
    end = DiagramNode(next_edges=[])
    _C_edge = DiagramEdge(next_node=end, non_terminal="c")
    _C_node = DiagramNode(next_edges=[_C_edge])
    additive_expression_prime = DiagramEdge(
        next_node=_C_node, non_terminal="additive_expression_prime"
    )

    return DiagramNode(next_edges=[additive_expression_prime], is_first=True)


def simple_expression_zegond_diagram():
    end = DiagramNode(next_edges=[])
    _C_edge = DiagramEdge(next_node=end, non_terminal="c")
    _C_node = DiagramNode(next_edges=[_C_edge])
    additive_expression_zegond = DiagramEdge(
        next_node=_C_node, non_terminal="additive_expression_zegond"
    )

    return DiagramNode(next_edges=[additive_expression_zegond], is_first=True)


def H_diagram():
    end = DiagramNode(next_edges=[])
    _C_edge = DiagramEdge(next_node=end, non_terminal="c")
    _C_node = DiagramNode(next_edges=[_C_edge])
    _D_edge = DiagramEdge(next_node=_C_node, non_terminal="d")
    _D_node = DiagramNode(next_edges=[_D_edge])
    _G_edge = DiagramEdge(next_node=_D_node, non_terminal="g")

    dummy_edge = DiagramEdge(next_node=end, terminal="ε", action_symbols=["assign"])
    dummy_node = DiagramNode(next_edges=[dummy_edge])
    expression = DiagramEdge(next_node=dummy_node, non_terminal="expression")
    expression_node = DiagramNode(next_edges=[expression])
    equal = DiagramEdge(next_node=expression_node, terminal="=")

    return DiagramNode(next_edges=[equal, _G_edge], is_first=True)


def B_diagram():
    end = DiagramNode(next_edges=[])

    _H_edge = DiagramEdge(
        next_node=end, non_terminal="h", action_symbols=["set_array_address"]
    )
    _H_node = DiagramNode(next_edges=[_H_edge])
    close_par = DiagramEdge(next_node=_H_node, terminal="]")
    close_par_node = DiagramNode(next_edges=[close_par])
    expression = DiagramEdge(next_node=close_par_node, non_terminal="expression")
    expression_node = DiagramNode(next_edges=[expression])
    open_par = DiagramEdge(next_node=expression_node, terminal="[")

    dummy_edge = DiagramEdge(next_node=end, terminal="ε", action_symbols=["assign"])
    dummy_node = DiagramNode(next_edges=[dummy_edge])
    expression = DiagramEdge(next_node=dummy_node, non_terminal="expression")
    expression_node = DiagramNode(next_edges=[expression])
    equal = DiagramEdge(next_node=expression_node, terminal="=")

    simple_expression_prime = DiagramEdge(
        next_node=end, non_terminal="simple_expression_prime"
    )

    return DiagramNode(
        next_edges=[open_par, equal, simple_expression_prime], is_first=True
    )


def expression_diagram():
    end = DiagramNode(next_edges=[])
    _B_edge = DiagramEdge(next_node=end, non_terminal="b")
    _B_node = DiagramNode(next_edges=[_B_edge])
    _id = DiagramEdge(next_node=_B_node, terminal="ID", action_symbols=["padd"])

    simple_expression_zegond = DiagramEdge(
        next_node=end, non_terminal="simple_expression_zegond"
    )

    return DiagramNode(next_edges=[simple_expression_zegond, _id], is_first=True)


def return_stmt_prime_diagram():
    end = DiagramNode(next_edges=[])

    semicolon_2 = DiagramEdge(
        next_node=end, terminal=";", action_symbols=["assign_to_func", "_return"]
    )
    semicolon_2_node = DiagramNode(next_edges=[semicolon_2])
    expression = DiagramEdge(next_node=semicolon_2_node, non_terminal="expression")

    semicolon = DiagramEdge(next_node=end, terminal=";", action_symbols=['_return'])

    return DiagramNode(next_edges=[semicolon, expression], is_first=True)


def return_stmt_diagram():
    end = DiagramNode(next_edges=[])
    return_stmt_prime = DiagramEdge(next_node=end, non_terminal="return_stmt_prime")
    statement_node = DiagramNode(next_edges=[return_stmt_prime])
    _return = DiagramEdge(next_node=statement_node, terminal="return")

    return DiagramNode(next_edges=[_return], is_first=True)


def iteration_stmt_diagram():
    end = DiagramNode(next_edges=[])
    close_bracket = DiagramEdge(next_node=end, terminal=")", action_symbols=["until"])
    close_bracket_node = DiagramNode(next_edges=[close_bracket])
    expression = DiagramEdge(next_node=close_bracket_node, non_terminal="expression")
    expression_node = DiagramNode(next_edges=[expression])
    open_bracket = DiagramEdge(next_node=expression_node, terminal="(")
    open_bracket_node = DiagramNode(next_edges=[open_bracket])
    until = DiagramEdge(next_node=open_bracket_node, terminal="until")
    until_node = DiagramNode(next_edges=[until])
    statement = DiagramEdge(
        next_node=until_node, non_terminal="statement", action_symbols=["label"]
    )
    statement_node = DiagramNode(next_edges=[statement])
    repeat = DiagramEdge(next_node=statement_node, terminal="repeat")

    return DiagramNode(next_edges=[repeat], is_first=True)


def else_stmt_diagram():
    end = DiagramNode(next_edges=[])
    endif = DiagramEdge(next_node=end, terminal="endif", action_symbols=["jp"])
    endif_node = DiagramNode(next_edges=[endif])
    statement = DiagramEdge(next_node=endif_node, non_terminal="statement")
    statement_node = DiagramNode(next_edges=[statement])
    _else = DiagramEdge(
        next_node=statement_node, terminal="else", action_symbols=["jpf_save"]
    )

    endif_2 = DiagramEdge(next_node=end, terminal="endif", action_symbols=["jpf"])

    return DiagramNode(next_edges=[_else, endif_2], is_first=True)


def selection_stmt_diagram():
    end = DiagramNode(next_edges=[])
    else_stmt = DiagramEdge(next_node=end, non_terminal="else_stmt")
    else_stmt_node = DiagramNode(next_edges=[else_stmt])
    statement = DiagramEdge(next_node=else_stmt_node, non_terminal="statement")
    statement_node = DiagramNode(next_edges=[statement])
    close_bracket = DiagramEdge(
        next_node=statement_node, terminal=")", action_symbols=["save"]
    )
    close_bracket_node = DiagramNode(next_edges=[close_bracket])
    expression = DiagramEdge(next_node=close_bracket_node, non_terminal="expression")
    expression_node = DiagramNode(next_edges=[expression])
    open_bracket = DiagramEdge(
        next_node=expression_node, terminal="(", action_symbols=["if_start"]
    )
    open_bracket_node = DiagramNode(next_edges=[open_bracket])
    _if = DiagramEdge(next_node=open_bracket_node, terminal="if")

    return DiagramNode(next_edges=[_if], is_first=True)


def expression_stmt_diagram():
    end = DiagramNode(next_edges=[])

    semicolon = DiagramEdge(next_node=end, terminal=";")

    semicolon_2 = DiagramEdge(next_node=end, terminal=";", action_symbols=["_break"])
    semicolon_node = DiagramNode(next_edges=[semicolon_2])
    _break = DiagramEdge(next_node=semicolon_node, terminal="break")

    semicolon_3 = DiagramEdge(next_node=end, terminal=";", action_symbols=["pop"])
    semicolon_node_2 = DiagramNode(next_edges=[semicolon_3])
    expression = DiagramEdge(next_node=semicolon_node_2, non_terminal="expression")

    return DiagramNode(next_edges=[semicolon, _break, expression], is_first=True)


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
        ],
        is_first=True,
    )


def statement_list_diagram():
    end = DiagramNode(next_edges=[])
    statement_list = DiagramEdge(next_node=end, non_terminal="statement_list")
    statement_list_node = DiagramNode(next_edges=[statement_list])
    statement = DiagramEdge(next_node=statement_list_node, non_terminal="statement")

    epsilon_node = DiagramEdge(next_node=end, terminal="ε")

    return DiagramNode(next_edges=[statement, epsilon_node], is_first=True)


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

    return DiagramNode(next_edges=[open_bracket], is_first=True)


def param_prime_diagram():
    end = DiagramNode(next_edges=[])
    close_bracket = DiagramEdge(
        next_node=end, terminal="]", action_symbols=["param_added", "make_var_array"] #TODO
    )
    close_bracket_node = DiagramNode(next_edges=[close_bracket])
    open_bracket = DiagramEdge(next_node=close_bracket_node, terminal="[")

    epsilon_node = DiagramEdge(
        next_node=end, terminal="ε", action_symbols=["param_added"]
    )

    return DiagramNode(next_edges=[open_bracket, epsilon_node], is_first=True)


def param_diagram():
    end = DiagramNode(next_edges=[])
    param_prime = DiagramEdge(next_node=end, non_terminal="param_prime")
    decl = DiagramNode(next_edges=[param_prime])
    decl_edge = DiagramEdge(next_node=decl, non_terminal="declaration_initial")

    return DiagramNode(next_edges=[decl_edge], is_first=True)


def param_list_diagram():
    end = DiagramNode(next_edges=[])
    param_list = DiagramEdge(next_node=end, non_terminal="param_list")
    param_list_node = DiagramNode(next_edges=[param_list])
    param = DiagramEdge(next_node=param_list_node, non_terminal="param")
    param_node = DiagramNode(next_edges=[param])
    comma = DiagramEdge(next_node=param_node, terminal=",")

    epsilon_node = DiagramEdge(next_node=end, terminal="ε")

    return DiagramNode(next_edges=[comma, epsilon_node], is_first=True)


def params_diagram():
    end = DiagramNode(next_edges=[])
    param_list = DiagramEdge(next_node=end, non_terminal="param_list")
    param_list_node = DiagramNode(next_edges=[param_list])
    param_prime = DiagramEdge(next_node=param_list_node, non_terminal="param_prime")
    param_prime_node = DiagramNode(next_edges=[param_prime])
    _id = DiagramEdge(
        next_node=param_prime_node,
        terminal="ID",
        action_symbols=["push_int", "padd", "pdeclare"],
    )
    id_node = DiagramNode(next_edges=[_id])
    _int = DiagramEdge(next_node=id_node, terminal="int")

    _void = DiagramEdge(
        next_node=end,
        terminal="void",
    )

    return DiagramNode(next_edges=[_int, _void], is_first=True)


def type_specifier_diagram():
    end = DiagramNode(next_edges=[])
    _int = DiagramEdge(next_node=end, terminal="int", action_symbols=["push_int"])

    _void = DiagramEdge(next_node=end, terminal="void", action_symbols=["push_void"])

    return DiagramNode(next_edges=[_int, _void], is_first=True)


def fun_declaration_prime():
    end = DiagramNode(next_edges=[])

    dummy_edge = DiagramEdge(
        next_node=end,
        terminal="ε",
        action_symbols=["_return", "end_scope", "end_function"],
    )
    dummy_node = DiagramNode(next_edges=[dummy_edge])
    compound_stmt = DiagramEdge(
        next_node=dummy_node,
        non_terminal="compound_stmt",
        action_symbols=["set_func_start"],
    )
    compound_stmt_node = DiagramNode(next_edges=[compound_stmt])
    close_par = DiagramEdge(next_node=compound_stmt_node, terminal=")")
    close_par_node = DiagramNode(next_edges=[close_par])
    params = DiagramEdge(
        next_node=close_par_node,
        non_terminal="params",
        action_symbols=["declare_function", "new_scope"],
    )
    params_node = DiagramNode(next_edges=[params])
    open_par = DiagramEdge(next_node=params_node, terminal="(")
    return DiagramNode(next_edges=[open_par], is_first=True)


def var_declaration_prime_diagram():
    end = DiagramNode(next_edges=[])

    semicolon = DiagramEdge(next_node=end, terminal=";", action_symbols=["var"])

    semicolon_2 = DiagramEdge(
        next_node=end, terminal=";", action_symbols=["make_var_array", "declare_global_arr"]
    )
    semicolon_2_node = DiagramNode(next_edges=[semicolon_2])
    close_t = DiagramEdge(next_node=semicolon_2_node, terminal="]")
    num_node = DiagramNode(next_edges=[close_t])
    num = DiagramEdge(next_node=num_node, terminal="NUM", action_symbols=["padd"])
    open_t_node = DiagramNode(next_edges=[num])
    open_t = DiagramEdge(next_node=open_t_node, terminal="[")

    return DiagramNode(next_edges=[semicolon, open_t], is_first=True)


def declaration_prime_diagram():
    end = DiagramNode(next_edges=[])
    fun_declaration_prime = DiagramEdge(
        next_node=end, non_terminal="fun_declaration_prime"
    )

    var_declaration_prime = DiagramEdge(
        next_node=end, non_terminal="var_declaration_prime"
    )

    return DiagramNode(
        next_edges=[fun_declaration_prime, var_declaration_prime], is_first=True
    )


def declaration_initial_diagram():
    end = DiagramNode(next_edges=[])
    _id = DiagramEdge(next_node=end, terminal="ID", action_symbols=["padd","pdeclare"])
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
    return DiagramNode(next_edges=[declaration_initial], is_first=True)


def declaration_list_diagram():
    end = DiagramNode(next_edges=[])
    declaration_list = DiagramEdge(next_node=end, non_terminal="declaration_list")
    declaration_list_node = DiagramNode(next_edges=[declaration_list])
    declaration = DiagramEdge(
        next_node=declaration_list_node, non_terminal="declaration"
    )

    epsilon_node = DiagramEdge(next_node=end, terminal="ε")

    return DiagramNode(next_edges=[declaration, epsilon_node], is_first=True)


def program_diagram():
    end = DiagramNode(next_edges=[])
    dollar = DiagramEdge(next_node=end, terminal="$")
    dollar_node = DiagramNode(next_edges=[dollar])
    declaration_list = DiagramEdge(
        next_node=dollar_node, non_terminal="declaration_list"
    )
    return DiagramNode(next_edges=[declaration_list], is_first=True)
