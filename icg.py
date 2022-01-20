import os

from black import json
from scanner import Scanner, Token, TokenType
from symbol_table import FuncOrVar, SymbolTable, SymbolTableRow, SymbolTableRowType
from utils import write_three_address_codes_to_file, write_semantic_errors
from function_table import FunctionTable


class IntermidateCodeGenerator:
    def __init__(
        self, symbol_table: SymbolTable, function_table: FunctionTable, scanner: Scanner
    ) -> None:
        self.semantic_stack = []
        self.semantic_errors = []
        self.three_addres_codes = {}
        self.i = 0
        self.debug = False #

        self.function_table: FunctionTable = function_table
        self.symbol_table: SymbolTable = symbol_table
        self.scanner: Scanner = scanner

        self.current_function_address = None
        self.arg_counter = -1
        self.func_call_stack = []
        self.retrun_stack = []
        self.main_added = False
        self.is_inside_function_declaration = False

        self.retrun_temp = self.symbol_table.get_temp()

        self.inside_if = False

        self.init_program()

    def init_program(self):
        self.add_three_address_code(f"(ASSIGN, #0, {self.retrun_temp}, )")
        self.add_three_address_code("", increase_i=True)  # for later jp to main
        self.add_output_function()

    def add_output_function(self) -> None:
        self.symbol_table.insert("output", is_declred=True)
        output_address = self.symbol_table.get_address("output")
        output_row = self.symbol_table.reverse_address(output_address)
        output_input_param = self.symbol_table.get_temp()

        self.function_table.func_declare(output_row, output_address, "void")
        self.function_table.add_param(
            output_address, "a", "int", output_input_param, False
        )
        self.function_table.funcs[output_address]["start_address"] = self.i
        self.add_three_address_code(f"(PRINT, {output_input_param}, ,)")
        self.add_three_address_code(f"(JP, @{self.retrun_temp}, , )")

    # functions
    def code_gen(self, action_symbol, current_token: Token):
        if self.debug:
            print(self.semantic_stack, action_symbol, current_token.lexeme, self.scanner.line_number)
        getattr(self, action_symbol)(current_token)

    def add_three_address_code(
        self, text: str, index: int = None, increase_i: bool = True
    ) -> None:
        self.three_addres_codes[index if index else self.i] = text
        self.i += 1 if increase_i else 0

    def save_to_file(self):
        print("ss stack at the end : ", self.semantic_stack)
        print("Symbol table : ", self.symbol_table.table)
        if len(self.semantic_errors) != 0:
            self.three_addres_codes = {}
        write_three_address_codes_to_file(self.three_addres_codes)
        write_semantic_errors(self.semantic_errors)

    def run_output(self):
        os.system("./tester_Linux.out")

    def func_arg_is_array(self, arg_address):
        current_func_info = self.function_table.funcs[self.current_function_address]
        if arg_address not in current_func_info["params_address"]:
            return False
        arg_index = current_func_info["params_address"].index(arg_address)
        is_arg_array = current_func_info["params_array"][arg_index]
        return is_arg_array

    # Actions
    def padd(self, current_token: Token):
        if current_token.type == TokenType.ID.name:
            if not self.is_inside_function_declaration:
                self.semantic_stack.append(
                    self.symbol_table.get_address(current_token.lexeme)
                )
            else:
                address = self.symbol_table.insert(
                    current_token.lexeme, is_declred=True
                )
                self.semantic_stack.append(address)

        elif current_token.type == TokenType.NUM.name:
            self.semantic_stack.append(f"#{current_token.lexeme}")
        elif current_token.type == TokenType.SYMBOL.name:
            self.semantic_stack.append(current_token.lexeme)

    def assign(self, current_token: Token):
        src = self.semantic_stack.pop()
        dst = self.semantic_stack[-1]
        self.add_three_address_code(f"(ASSIGN, {src}, {dst}, )")

    def op(self, current_token: Token):
        operand_map = {"+": "ADD", "-": "SUB", "*": "MULT", "<": "LT", "==": "EQ"}

        second_operand = self.semantic_stack.pop()
        operand = operand_map[self.semantic_stack.pop()]
        first_operand = self.semantic_stack.pop()

        self.check_operand_missmatch(first_operand, second_operand)

        if operand == "LT" and "@" in str(first_operand):
            self.add_three_address_code(f"(PRINT, {first_operand[1:]}, ,)")

        op_result = self.symbol_table.get_temp()

        self.add_three_address_code(
            f"({operand}, {first_operand}, {second_operand}, {op_result})"
        )

        self.semantic_stack.append(op_result)

    def label(self, current_token: Token):
        self.semantic_stack.append(self.i)

    def until(self, current_token: Token):
        condition = self.semantic_stack.pop()
        target = self.semantic_stack.pop()
        self.add_three_address_code(f"(JPF, {condition}, {target}, )")

    def jp(self, current_token: Token):
        self.add_three_address_code(
            f"(JP, {self.i}, , )", index=self.semantic_stack.pop(), increase_i=False
        )

    def jpf_save(self, current_token: Token):
        pb_empty_place = self.semantic_stack.pop()
        condition = self.semantic_stack.pop()
        self.semantic_stack.append(self.i)

        self.add_three_address_code(
            text=f"(JPF, {condition}, {self.i + 1}, )", index=pb_empty_place
        )

    def jpf(self, current_token: Token):
        pb_empty_place = self.semantic_stack.pop()
        condition = self.semantic_stack.pop()
        self.add_three_address_code(
            text=f"(JPF, {condition}, {self.i}, )",
            index=pb_empty_place,
            increase_i=False,
        )

    def save(self, current_token: Token):
        self.semantic_stack.append(self.i)
        self.i += 1

    def declare_function(self, current_token: Token):
        self.is_inside_function_declaration = True

        function_address = self.semantic_stack[-1]
        function_row = self.symbol_table.reverse_address(function_address)
        function_row.is_declred = True
        function_row.func_or_var = FuncOrVar.func

        self.function_table.func_declare(function_row, function_address, "void")
        if function_row.lexeme == "main":
            self.add_three_address_code(
                f"(JP, {self.i}, , )", index=1, increase_i=False
            )
            self.main_added = True

        self.function_table.func_declare(
            function_row, function_address, self.semantic_stack[-2]
        )

        self.current_function_address = function_address

    def var(self, current_token: Token):
        var = self.semantic_stack.pop()
        var_type = self.semantic_stack.pop()
        self.add_three_address_code(f"(ASSIGN, #0, {var}, )")

    def declare_global_arr(self, current_token: Token):
        size = int(self.semantic_stack.pop()[1:])  # remove # from int
        var = self.semantic_stack.pop()
        var_type = self.semantic_stack.pop()

        for i in range(size):
            self.add_three_address_code(f"(ASSIGN, #0, {var + i * 4}, )")
            self.symbol_table.get_temp()

    def push_int(self, current_token: Token):
        self.semantic_stack.append("int")

    def push_void(self, current_token: Token):
        self.semantic_stack.append("void")

    def param_added(self, current_token: Token):
        func = self.semantic_stack[-3]
        is_array = current_token.lexeme == "]"
        param_name = None
        for i in self.symbol_table.get_rows():
            if i.address == self.semantic_stack[-1]:
                param_name = i.lexeme
                break
        self.function_table.add_param(
            func,
            param_name,
            self.semantic_stack[-2],
            self.semantic_stack[-1],
            is_array,
        )
        self.semantic_stack.pop()
        self.semantic_stack.pop()

    def pop(self, current_token: Token):
        self.semantic_stack.pop()

    def _break(self, current_token: Token):
        if self.inside_if:
            self.add_three_address_code(f"(JP, @{self.semantic_stack[-7]}, , )")
            self.inside_if = False
        else:
            self.add_three_address_code(f"(JP, @{self.semantic_stack[-5]}, , )")

    def assign_to_func(self, current_token: Token):
        if not self.main_added:
            self.add_three_address_code(
                f"(ASSIGN, {self.semantic_stack.pop()}, {self.current_function_address}, )"
            )

    def set_array_address(self, current_token: Token):
        temp = self.symbol_table.get_temp()
        offset = self.semantic_stack.pop()
        base = self.semantic_stack.pop()

        self.add_three_address_code(f"(MULT, #4, {offset}, {temp})")

        if self.func_arg_is_array(base):
            self.add_three_address_code(f"(ADD, {base}, {temp}, {temp})")
        else:
            self.add_three_address_code(f"(ADD, #{base}, {temp}, {temp})")
        self.semantic_stack.append(f"@{temp}")

    def func_call_started(self, current_token: Token):
        func_name = self.semantic_stack[-1]
        self.func_number_of_args = len(self.function_table.funcs[func_name]["params"])
        self.arg_counter = 0
        self.func_call_stack.append(func_name)

    def func_call_ended(self, current_token: Token):
        function_address = self.func_call_stack.pop()
        temp = self.symbol_table.get_temp()
        self.add_three_address_code(f"(ASSIGN, #0, {function_address}, )")
        self.add_three_address_code(f"(ASSIGN, #0, {temp}, )")
        self.add_three_address_code(f"(ASSIGN, {self.retrun_temp}, {temp}, )")
        self.add_three_address_code(f"(ASSIGN, #{self.i + 2}, {self.retrun_temp}, )")
        self.add_three_address_code(
            f"(JP, {self.function_table.funcs[function_address]['start_address']}, , )"
        )
        self.add_three_address_code(f"(ASSIGN, {temp}, {self.retrun_temp},  )")

        self.arg_counter = 0

    def push_arg(self, current_token: Token):
        function_info = self.function_table.funcs[self.func_call_stack[-1]]
        try:
            self.semantic_stack.append(
                function_info["params_address"][self.arg_counter]
            )
            self.arg_counter += 1
        except IndexError:
            self.semantic_stack.append("#20")  # TODO change this temp
            function_name = function_info["name"].lexeme
            self.semantic_errors.append(
                f"#{self.scanner.line_number} : Semantic Error! Mismatch in numbers of arguments of '{function_name}'."
            )

    def if_start(self, current_token: Token):
        self.inside_if = True

    def end_function(self, current_token: Token):
        function_address = self.semantic_stack.pop()
        function_type = self.semantic_stack.pop()
        # maybe we should do something here

    def set_func_start(self, current_token: Token):
        self.is_inside_function_declaration = False

        self.function_table.funcs[self.semantic_stack[-1]]["start_address"] = self.i

    def new_scope(self, current_token: Token):
        self.symbol_table.scope_stack.append(self.scanner.line_number)

    def end_scope(self, current_token: Token):
        self.symbol_table.scope_stack.pop()

    def _return(self, current_token: Token):
        function_name = self.symbol_table.reverse_address(self.current_function_address)
        if function_name.lexeme != "main":
            self.add_three_address_code(f"(JP, @{self.retrun_temp}, , )")

    def assign_arg(self, current_token: Token):
        src = self.semantic_stack.pop()
        dst = self.semantic_stack.pop()

        function_info = self.function_table.funcs[self.func_call_stack[-1]]
        current_arg_is_array = function_info["params_array"][self.arg_counter - 1]

        self.check_missmatch_type(src, function_info)

        if current_arg_is_array:
            self.add_three_address_code(f"(ASSIGN, #{src}, {dst}, )")
        else:
            self.add_three_address_code(f"(ASSIGN, {src}, {dst}, )")

    # semantic errors
    def check_missmatch_type(self, src, function_info):
        current_arg_is_array = function_info["params_array"][self.arg_counter - 1]
        var = self.symbol_table.reverse_address(src)
        var_type = "int" if var == None else var.type.name
        

        arg_type = (
            function_info["params_type"][self.arg_counter - 1]
            if function_info["params_array"][self.arg_counter - 1] == False
            else "array"
        )
        function_name = function_info["name"].lexeme
        if current_arg_is_array and var_type != SymbolTableRowType.array.name:
            self.semantic_errors.append(
                f"#{self.scanner.line_number} : Semantic Error! Mismatch in type of argument {self.arg_counter} of "
                + f"'{function_name}'. Expected 'array' but got '{var_type}' instead."
            )
        elif arg_type != var_type:
            self.semantic_errors.append(
                f"#{self.scanner.line_number} : Semantic Error! Mismatch in type of argument {self.arg_counter} of "
                + f"'{function_name}'. Expected '{arg_type}' but got '{var_type}' instead."
            )

    def check_operand_missmatch(self, first, second):
        first_row = self.symbol_table.reverse_address(first)
        first_row = first_row.type.name if first_row else "int"

        second_row = self.symbol_table.reverse_address(second)
        second_row = second_row.type.name if second_row else "int"

        if first_row != second_row:
            self.semantic_errors.append(
                f"#{self.scanner.line_number} : Semantic Error! Type mismatch in operands, "
                + f"Got {second_row} instead of {first_row}."
            )

    def check_not_void(self, row: SymbolTableRow):
        if row.type == SymbolTableRowType.void and row.func_or_var == FuncOrVar.var:
            self.semantic_errors.append(
                f"#{self.scanner.line_number} : Semantic Error! Illegal type of void for '{row.lexeme}'."
            )

    def pdeclare(self, current_token: Token):
        var_type = self.semantic_stack[-2]
        var_row = self.symbol_table.reverse_address(self.semantic_stack[-1])
        var_row.type = (
            SymbolTableRowType.int
            if var_type == SymbolTableRowType.int.name
            else SymbolTableRowType.void
        )
        var_row.is_declred = True

        self.check_not_void(var_row)

    def make_var_array(self, current_token: Token):
        var_row = self.symbol_table.reverse_address(self.semantic_stack[-2])
        var_row.type = SymbolTableRowType.array

    def array_param_added(self, current_token: Token):
        var_row = self.symbol_table.reverse_address(self.semantic_stack[-1])
        var_row.type = SymbolTableRowType.array
        self.param_added(current_token)

    def check_declare(self, current_token: Token):
        address = self.semantic_stack[-1]
        row = self.symbol_table.reverse_address(address)
        if not row.is_declred:
            self.semantic_errors.append(
                f"#{self.scanner.line_number} : Semantic Error! '{row.lexeme}' is not defined."
            )
            row.type = SymbolTableRowType.int
