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

    # 9
    # end = ParseTreeNode(next_edges=[])
    # param_list = ParseTreeEdge(next_node=end, non_terminal='param_list')
    # param_list_node = ParseTreeNode(next_edges=[param_list])
    # param_prime = ParseTreeEdge(next_node=param_list_node, non_terminal='param_prime')
    # param_prime_node = ParseTreeNode(next_edges=[param_prime])
    # _id = ParseTreeEdge(next_node=param_prime_node, terminal="ID")
    # id_node = ParseTreeNode(next_edges=[_id])
    # _int = ParseTreeEdge(next_node=id_node, terminal="int")

    # _void = ParseTreeEdge(next_node=end, terminal="void")

    # start_node = ParseTreeNode(next_edges=[_int, _void])
    # first_nodes.append(start_node)

    # 10
    # end = ParseTreeNode(next_edges=[])
    # param_list = ParseTreeEdge(next_node=end, non_terminal='param_list')
    # param_list_node = ParseTreeNode(next_edges=[param_list])
    # param = ParseTreeEdge(next_node=param_list_node, non_terminal='param')
    # param_node = ParseTreeNode(next_edges=[param])
    # comma = ParseTreeEdge(next_node=param_node, terminal=",")

    # epsilon_node = ParseTreeEdge(next_node=end, terminal="ε")

    # start_node = ParseTreeNode(next_edges=[comma, epsilon_node])
    # first_nodes.append(start_node)

    # 11
    # end = ParseTreeNode(next_edges=[])
    # param_prime = ParseTreeEdge(next_node=end, non_terminal='param_prime')
    # param_prime_node = ParseTreeNode(next_edges=[param_prime])

    # start_node = ParseTreeNode(next_edges=[param_prime_node])
    # first_nodes.append(start_node)

    # 12
    # end = ParseTreeNode(next_edges=[])
    # close_bracket = ParseTreeEdge(next_node=end, terminal=']')
    # close_bracket_node = ParseTreeNode(next_edges=[close_bracket])
    # open_bracket = ParseTreeEdge(next_node=close_bracket_node, terminal='[')
    # open_bracket_node = ParseTreeNode(next_edges=[open_bracket])

    # epsilon_node = ParseTreeEdge(next_node=end, terminal="ε")

    # start_node = ParseTreeNode(next_edges=[open_bracket_node, epsilon_node])
    # first_nodes.append(start_node)

    # 13
    # end = ParseTreeNode(next_edges=[])
    # close_bracket = ParseTreeEdge(next_node=end, terminal="}")
    # close_bracket_node = ParseTreeNode(next_edges=[close_bracket])
    # statement_list = ParseTreeEdge(next_node=close_bracket_node, non_terminal="statement_list")
    # statement_list_node = ParseTreeNode(next_edges=[statement_list])
    # declarion_list = ParseTreeEdge(next_node=statement_list_node, non_terminal="declarion_list")
    # declarion_list_node = ParseTreeNode(next_edges=[declarion_list])
    # open_bracket = ParseTreeEdge(next_node=declarion_list_node, terminal="{")

    # start_node = ParseTreeNode(next_edges=[open_bracket])
    # first_nodes.append(start_node)

    # 14
    # end = ParseTreeNode(next_edges=[])
    # statement_list = ParseTreeEdge(next_node=end, non_terminal='statement_list')
    # statement_list_node = ParseTreeNode(next_edges=[statement_list])
    # statement_bracket = ParseTreeEdge(next_node=statement_list_node, non_terminal='statement')
    # statement_node = ParseTreeNode(next_edges=[statement_bracket])

    # epsilon_node = ParseTreeEdge(next_node=end, terminal="ε")

    # start_node = ParseTreeNode(next_edges=[statement_node, epsilon_node])
    # first_nodes.append(start_node)

    # 15
    # end = ParseTreeNode(next_edges=[])

    # expression_stmt = ParseTreeEdge(next_node=end, non_terminal="expression_stmt")

    # compund_stmt = ParseTreeEdge(next_node=end, non_terminal="compund_stmt")

    # selection_stmt = ParseTreeEdge(next_node=end, non_terminal="selection_stmt")

    # iteration_stmt = ParseTreeEdge(next_node=end, non_terminal="iteration_stmt")

    # return_stmt = ParseTreeEdge(next_node=end, non_terminal="statement_list")

    # start_node = ParseTreeNode(
    #     next_edges=[
    #         expression_stmt,
    #         compund_stmt,
    #         selection_stmt,
    #         iteration_stmt,
    #         return_stmt,
    #     ]
    # )
    # first_nodes.append(start_node)

    # 16
    # end = ParseTreeNode(next_edges=[])

    # semicolon = ParseTreeEdge(next_node=end, terminal=";")

    # semicolon_2 = ParseTreeEdge(next_node=end, terminal=";")
    # semicolon_node = ParseTreeNode(next_edges=[semicolon_2])
    # _break = ParseTreeEdge(next_node=semicolon_node, terminal="break")

    # semicolon_3 = ParseTreeEdge(next_node=end, terminal=";")
    # semicolon_node_2 = ParseTreeNode(next_edges=[semicolon_3])
    # expression = ParseTreeEdge(next_node=semicolon_node_2, non_terminal="expression")

    # start_node = ParseTreeNode(next_edges=[semicolon, _break, expression])
    # first_nodes.append(start_node)

    # 17
    # end = ParseTreeNode(next_edges=[])
    # else_stmt = ParseTreeEdge(next_node=end, non_terminal="else_stmt")
    # else_stmt_node = ParseTreeNode(next_edges=[else_stmt])
    # statement = ParseTreeEdge(next_node=else_stmt_node, non_terminal="statement")
    # statement_node = ParseTreeNode(next_edges=[statement])
    # close_bracket = ParseTreeEdge(next_node=statement_node, terminal=')')
    # close_bracket_node = ParseTreeNode(next_edges=[close_bracket])
    # expression = ParseTreeEdge(next_node=close_bracket_node, non_terminal="expression")
    # expression_node = ParseTreeNode(next_edges=[expression])
    # open_bracket = ParseTreeEdge(next_node=expression_node, terminal='(')
    # open_bracket_node = ParseTreeNode(next_edges=[open_bracket])
    # _if = ParseTreeEdge(next_node=open_bracket_node, terminal="if")

    # start_node = ParseTreeNode(next_edges=[_if])
    # first_nodes.append(start_node)

    # 18
    # end = ParseTreeNode(next_edges=[])
    # endif = ParseTreeEdge(next_node=end, terminal="endif")
    # endif_node = ParseTreeNode(next_edges=[endif])
    # statement = ParseTreeEdge(next_node=endif_node, non_terminal="statement")
    # statement_node = ParseTreeNode(next_edges=[statement])
    # _else = ParseTreeEdge(next_node=statement_node, terminal="else")

    # endif_2 = ParseTreeEdge(next_node=end, terminal="endif")

    # start_node = ParseTreeNode(next_edges=[_else, endif_2])
    # first_nodes.append(start_node)

    # 19
    # end = ParseTreeNode(next_edges=[])
    # close_bracket = ParseTreeEdge(next_node=end, terminal=')')
    # close_bracket_node = ParseTreeNode(next_edges=[close_bracket])
    # expression = ParseTreeEdge(next_node=close_bracket_node, non_terminal="expression")
    # expression_node = ParseTreeNode(next_edges=[expression])
    # open_bracket = ParseTreeEdge(next_node=expression_node, terminal='(')
    # open_bracket_node = ParseTreeNode(next_edges=[open_bracket])
    # until = ParseTreeEdge(next_node=open_bracket_node, terminal="until")
    # until_node = ParseTreeNode(next_edges=[until])
    # statement = ParseTreeEdge(next_node=until_node, non_terminal="statement")
    # statement_node = ParseTreeNode(next_edges=[statement])
    # repeat = ParseTreeEdge(next_node=statement_node, terminal="repeat")

    # start_node = ParseTreeNode(next_edges=[repeat])
    # first_nodes.append(start_node)

    # 20
    # end = ParseTreeNode(next_edges=[])
    # return_stmt_prime = ParseTreeEdge(next_node=end, non_terminal="return_stmt_prime")
    # statement_node = ParseTreeNode(next_edges=[return_stmt_prime])
    # _return = ParseTreeEdge(next_node=statement_node, terminal="return")

    # start_node = ParseTreeNode(next_edges=[_return])
    # first_nodes.append(start_node)

    # 21
    # end = ParseTreeNode(next_edges=[])

    # semicolon_2 = ParseTreeEdge(next_node=end, terminal=";")
    # semicolon_2_node = ParseTreeNode(next_edges=[semicolon_2])
    # expression = ParseTreeEdge(next_node=semicolon_2_node, non_terminal="expression")

    # semicolon = ParseTreeEdge(next_node=end, terminal=";")

    # start_node = ParseTreeNode(next_edges=[semicolon, expression])
    # first_nodes.append(start_node)

    # 22
    # end = ParseTreeNode(next_edges=[])
    # _B_edge = ParseTreeEdge(next_node=end, non_terminal="B")
    # _B_node = ParseTreeNode(next_edges=[_B_edge])
    # _id = ParseTreeEdge(next_node=_B_node, terminal="ID")

    # simple_expression_zegond = ParseTreeEdge(next_node=end, non_terminal="simple_expression_zegond")

    # start_node = ParseTreeNode(next_edges=[simple_expression_zegond, _id])
    # first_nodes.append(start_node)

    # 23
    # end = ParseTreeNode(next_edges=[])

    # _H_edge = ParseTreeEdge(next_node=end, non_terminal="H")
    # _H_node = ParseTreeNode(next_edges=[_H_edge])
    # close_par = ParseTreeEdge(next_node=_H_node, terminal="]")
    # close_par_node = ParseTreeNode(next_edges=[close_par])
    # expression = ParseTreeEdge(next_node=close_par_node, non_terminal="expression")
    # expression_node = ParseTreeNode(next_edges=[expression])
    # open_par = ParseTreeEdge(next_node=expression_node, terminal="[")

    # expression_2 = ParseTreeEdge(next_node=end, non_terminal="expression")

    # simple_expression_prime = ParseTreeEdge(
    #     next_node=end, non_terminal="simple_expression_prime"
    # )

    # start_node = ParseTreeNode(
    #     next_edges=[simple_expression_prime, expression_2, open_par]
    # )
    # first_nodes.append(start_node)

    # 24
    # end = ParseTreeNode(next_edges=[])
    # _C_edge = ParseTreeEdge(next_node=end, non_terminal="C")
    # _C_node = ParseTreeNode(next_edges=[_C_edge])
    # _D_edge = ParseTreeEdge(next_node=_C_node, non_terminal="D")
    # _D_node = ParseTreeNode(next_edges=[_D_edge])
    # _G_edge = ParseTreeEdge(next_node=_D_node, non_terminal="G")

    # expression = ParseTreeEdge(next_node=end, non_terminal="expression")

    # start_node = ParseTreeNode(next_edges=[expression, _G_edge])
    # first_nodes.append(start_node)

    # 25
    # end = ParseTreeNode(next_edges=[])
    # _C_edge = ParseTreeEdge(next_node=end, non_terminal="C")
    # _C_node = ParseTreeNode(next_edges=[_C_edge])
    # additive_expression_zegond = ParseTreeEdge(
    #     next_node=_C_node, non_terminal="additive_expression_zegond"
    # )

    # start_node = ParseTreeNode(next_edges=[additive_expression_zegond])
    # first_nodes.append(start_node)

    # 26
    # end = ParseTreeNode(next_edges=[])
    # _C_edge = ParseTreeEdge(next_node=end, non_terminal="C")
    # _C_node = ParseTreeNode(next_edges=[_C_edge])
    # additive_expression_prime = ParseTreeEdge(
    #     next_node=_C_node, non_terminal="additive_expression_prime"
    # )

    # start_node = ParseTreeNode(next_edges=[additive_expression_prime])
    # first_nodes.append(start_node)

    # 27
    # end = ParseTreeNode(next_edges=[])
    # additive_expression = ParseTreeEdge(
    #     next_node=end, non_terminal="additive_expression"
    # )
    # additive_expression_node = ParseTreeNode(next_edges=[additive_expression])
    # relop = ParseTreeEdge(next_node=additive_expression_node, non_terminal="relop")

    # epsilon_node = ParseTreeEdge(next_node=end, terminal="ε")

    # start_node = ParseTreeNode(next_edges=[relop, epsilon_node])
    # first_nodes.append(start_node)

    # 28
    # end = ParseTreeNode(next_edges=[])
    # lower = ParseTreeEdge(next_node=end, terminal="<")

    # equal_1 = ParseTreeEdge(next_node=end, terminal="=")
    # equal_1_node = ParseTreeNode(next_edges=[equal_1])
    # equal_2 = ParseTreeEdge(next_node=equal_1_node, terminal="=")

    # start_node = ParseTreeNode(next_edges=[lower, equal_2])
    # first_nodes.append(start_node)

    # 29
    # end = ParseTreeNode(next_edges=[])
    # _D_edge = ParseTreeEdge(next_node=end, non_terminal="D")
    # _D_node = ParseTreeNode(next_edges=[_D_edge])
    # term = ParseTreeEdge(next_node=_D_node, non_terminal="term")

    # start_node = ParseTreeNode(next_edges=[term])
    # first_nodes.append(start_node)

    # 30
    # end = ParseTreeNode(next_edges=[])
    # _D_edge = ParseTreeEdge(next_node=end, non_terminal="D")
    # _D_node = ParseTreeNode(next_edges=[_D_edge])
    # term_prime = ParseTreeEdge(next_node=_D_node, non_terminal="term_prime")

    # start_node = ParseTreeNode(next_edges=[term_prime])
    # first_nodes.append(start_node)

    # 31
    # end = ParseTreeNode(next_edges=[])
    # _D_edge = ParseTreeEdge(next_node=end, non_terminal="D")
    # _D_node = ParseTreeNode(next_edges=[_D_edge])
    # term_zegond = ParseTreeEdge(next_node=_D_node, non_terminal="term_zegond")

    # start_node = ParseTreeNode(next_edges=[term_zegond])
    # first_nodes.append(start_node)

    # 32
    # end = ParseTreeNode(next_edges=[])
    # _D_edge = ParseTreeEdge(next_node=end, non_terminal="D")
    # _D_node = ParseTreeNode(next_edges=[_D_edge])
    # term = ParseTreeEdge(next_node=_D_node, non_terminal="term")
    # term_node = ParseTreeNode(next_edges=[term])
    # addop = ParseTreeEdge(next_node=term_node,non_terminal='addop')

    # epsilon_node = ParseTreeEdge(next_node=end, terminal="ε")

    # start_node = ParseTreeNode(next_edges=[addop, epsilon_node])
    # first_nodes.append(start_node)

    # 33
    # end = ParseTreeNode(next_edges=[])
    # plus = ParseTreeEdge(next_node=end, terminal="+")

    # minus = ParseTreeEdge(next_node=end, terminal="-")

    # start_node = ParseTreeNode(next_edges=[plus, minus])
    # first_nodes.append(start_node)

    # 34
    # end = ParseTreeNode(next_edges=[])
    # _G_edge = ParseTreeEdge(next_node=end, non_terminal="G")
    # _G_node = ParseTreeNode(next_edges=[_G_edge])
    # factor = ParseTreeEdge(next_node=_G_node, non_terminal="factor")

    # start_node = ParseTreeNode(next_edges=[factor])
    # first_nodes.append(start_node)

    # 35
    # end = ParseTreeNode(next_edges=[])
    # _G_edge = ParseTreeEdge(next_node=end, non_terminal="G")
    # _G_node = ParseTreeNode(next_edges=[_G_edge])
    # factor_prime = ParseTreeEdge(next_node=_G_node, non_terminal="factor_prime")

    # start_node = ParseTreeNode(next_edges=[factor_prime])
    # first_nodes.append(start_node)

    # 36
    # end = ParseTreeNode(next_edges=[])
    # _G_edge = ParseTreeEdge(next_node=end, non_terminal="G")
    # _G_node = ParseTreeNode(next_edges=[_G_edge])
    # factor_zegond = ParseTreeEdge(next_node=_G_node, non_terminal="factor_zegond")

    # start_node = ParseTreeNode(next_edges=[factor_zegond])
    # first_nodes.append(start_node)

    # 37
    # end = ParseTreeNode(next_edges=[])
    # _G_edge = ParseTreeEdge(next_node=end, non_terminal='G')
    # _G_node = ParseTreeNode(next_edges=[_G_edge])
    # factor = ParseTreeEdge(next_node=_G_node, non_terminal='factor')
    # factor_node = ParseTreeNode(next_edges=[factor])
    # star = ParseTreeEdge(next_node=factor_node, terminal="*")

    # epsilon_node = ParseTreeEdge(next_node=end, terminal="ε")

    # start_node = ParseTreeNode(next_edges=[star, epsilon_node])
    # first_nodes.append(start_node)

    # 38
    # end = ParseTreeNode(next_edges=[])
    # close_par = ParseTreeEdge(next_node=end, terminal=")")
    # close_par_node = ParseTreeNode(next_edges=[close_par])
    # expression = ParseTreeEdge(next_node=close_par_node, non_terminal="expression")
    # expression_node = ParseTreeNode(next_edges=[expression])
    # open_par = ParseTreeEdge(next_node=expression_node, terminal="(")

    # var_call_prime = ParseTreeEdge(next_node=end, non_terminal="var_call_prime")
    # var_call_prime_node = ParseTreeNode(next_edges=[var_call_prime])
    # id = ParseTreeEdge(next_node=var_call_prime_node, terminal="ID")

    # num = ParseTreeEdge(next_node=end, terminal="NUM")

    # start_node = ParseTreeNode(next_edges=[open_par, num, id])
    # first_nodes.append(start_node)

    # 39
    # end = ParseTreeNode(next_edges=[])
    # close_par = ParseTreeEdge(next_node=end, terminal=")")
    # close_par_node = ParseTreeNode(next_edges=[close_par])
    # args = ParseTreeEdge(next_node=close_par_node, non_terminal="args")
    # args_node = ParseTreeNode(next_edges=[args])
    # open_par = ParseTreeEdge(next_node=args_node, terminal="(")

    # var_prime = ParseTreeEdge(next_node=end, non_terminal="var_prime")

    # start_node = ParseTreeNode(next_edges=[open_par, var_prime])
    # first_nodes.append(start_node)

    # 40
    # end = ParseTreeNode(next_edges=[])
    # close_par = ParseTreeEdge(next_node=end, terminal="]")
    # close_par_node = ParseTreeNode(next_edges=[close_par])
    # expression = ParseTreeEdge(next_node=close_par_node, non_terminal="expression")
    # expression_node = ParseTreeNode(next_edges=[expression])
    # open_par = ParseTreeEdge(next_node=expression_node, terminal="[")

    # epsilon_node = ParseTreeEdge(next_node=end, terminal="ε")
    
    # start_node = ParseTreeNode(next_edges=[open_par, epsilon_node])
    # first_nodes.append(start_node)

    # 41
    # end = ParseTreeNode(next_edges=[])
    # close_par = ParseTreeEdge(next_node=end, terminal=")")
    # close_par_node = ParseTreeNode(next_edges=[close_par])
    # args = ParseTreeEdge(next_node=close_par_node, non_terminal="args")
    # args_node = ParseTreeNode(next_edges=[args])
    # open_par = ParseTreeEdge(next_node=args_node, terminal="(")

    # epsilon_node = ParseTreeEdge(next_node=end, terminal="ε")
    
    # start_node = ParseTreeNode(next_edges=[open_par, epsilon_node])
    # first_nodes.append(start_node)

    # 42
    # end = ParseTreeNode(next_edges=[])
    # close_par = ParseTreeEdge(next_node=end, terminal=")")
    # close_par_node = ParseTreeNode(next_edges=[close_par])
    # expression = ParseTreeEdge(next_node=close_par_node, non_terminal="expression")
    # expression_node = ParseTreeNode(next_edges=[expression])
    # open_par = ParseTreeEdge(next_node=expression_node, terminal="(")

    # num = ParseTreeEdge(next_node=end, terminal="NUM")
    
    # start_node = ParseTreeNode(next_edges=[open_par, num])
    # first_nodes.append(start_node)

    # 43
    # end = ParseTreeNode(next_edges=[])
    # arg_list = ParseTreeEdge(next_node=end,non_terminal='arg_list')

    # epsilon_node = ParseTreeEdge(next_node=end, terminal="ε")

    # start_node = ParseTreeNode(next_edges=[arg_list, epsilon_node])
    # first_nodes.append(start_node)

    # 44
    # end = ParseTreeNode(next_edges=[])
    # arg_list_prime = ParseTreeEdge(next_node=end, non_terminal="arg_list_prime")
    # arg_list_prime_node = ParseTreeNode(next_edges=[arg_list_prime])
    # expression = ParseTreeEdge(next_node=arg_list_prime_node, non_terminal="expression")

    # start_node = ParseTreeNode(next_edges=[expression])
    # first_nodes.append(start_node)

    # 45
    # end = ParseTreeNode(next_edges=[])
    # arg_list_prime = ParseTreeEdge(next_node=end, non_terminal='arg_list_prime')
    # arg_list_prime_node = ParseTreeNode(next_edges=[arg_list_prime])
    # expression = ParseTreeEdge(next_node=arg_list_prime_node, non_terminal='expression')
    # expression_node = ParseTreeNode(next_edges=[expression])
    # comma = ParseTreeEdge(next_node=expression_node, terminal=",")

    # epsilon_node = ParseTreeEdge(next_node=end, terminal="ε")

    # start_node = ParseTreeNode(next_edges=[comma, epsilon_node])
    # first_nodes.append(start_node)
    return


def add_firsts():
    with open("firsts.txt", "r") as file:
        a = list(map(str.split, file.readlines()))
    for line in a:
        first_dict[line[0]] = line[1:]
