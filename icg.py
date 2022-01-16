import os
from scanner import Token, TokenType
from symbol_table import SymbolTable
from utils import write_three_address_codes_to_file
from function_table import FunctionTable


class IntermidateCodeGenerator:
    def __init__(
        self, symbol_table: SymbolTable, function_table: FunctionTable
    ) -> None:
        self.semantic_stack = []
        self.three_addres_codes = {}
        self.i = 0
        self.debug = False
        self.function_table: FunctionTable = function_table

        self.symbol_table = symbol_table

        self.retrun_temp = self.symbol_table.get_temp()

        self.init_program()
        self.init_icg_variables()

    # init functions
    def init_icg_variables(self) -> None:
        self.main_added = False
        self.current_function_address = None
        self.arg_counter = -1
        self.func_call_stack = []

        self.inside_if = False
        self.break_bool = False

    def init_program(self):
        self.add_three_address_code(f"(ASSIGN, #0, {self.retrun_temp}, )")
        self.add_three_address_code("", increase_i=True)
        self.add_output_function()

    def add_output_function(self) -> None:
        self.symbol_table.insert("output", is_declred=True)
        output_address = self.symbol_table.get_address("output")
        output_input_param = self.symbol_table.get_temp()
        self.function_table.func_declare("output", output_address, "void")
        self.function_table.add_param(
            output_address, "a", "int", output_input_param, False
        )
        self.function_table.funcs[output_address]["start_address"] = self.i
        self.add_three_address_code(f"(PRINT, {output_input_param}, ,)")
        self.add_three_address_code(f"(JP, @{self.retrun_temp}, , )")

    # functions
    def code_gen(self, action_symbol, current_token: Token):
        if self.debug:
            print(self.semantic_stack, action_symbol, current_token.lexeme)
        getattr(self, action_symbol)(current_token)

    def add_three_address_code(
        self, text: str, index: int = None, increase_i: bool = True
    ) -> None:
        self.three_addres_codes[index if index else self.i] = text
        self.i += 1 if increase_i else 0

    def save_to_file(self):
        print("ss stack at the end : ", self.semantic_stack)
        print("Symbol table : ", self.symbol_table.table)
        write_three_address_codes_to_file(self.three_addres_codes)

    def run_output(self):
        os.system("./tester_Linux.out")

    # Actions
    def padd(self, current_token: Token):
        if current_token.type == TokenType.ID.name:
            if current_token.lexeme not in self.symbol_table.get_declared_symbols():
                print(f"Semantic error! not declared symbol : {current_token.lexeme}")
            self.semantic_stack.append(
                self.symbol_table.get_address(current_token.lexeme)
            )

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

        tmp_address = self.symbol_table.get_temp()

        self.add_three_address_code(
            f"({operand}, {first_operand}, {second_operand}, {tmp_address})"
        )

        self.semantic_stack.append(tmp_address)

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
        self.add_three_address_code(
            text=f"(JPF, {condition}, {self.i + 1}, )",
            index=pb_empty_place,
            increase_i=False,
        )

        self.semantic_stack.append(self.i)
        self.i += 1

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

    def declare_id(self, current_token: Token):
        self.symbol_table.get_symbol_record(current_token.lexeme).make_declared()
        self.add_three_address_code(
            f"(ASSIGN, #0, {self.symbol_table.get_address(current_token.lexeme)}, )"
        )

    def declare_function(self, current_token: Token):
        function_address = self.semantic_stack[-1]
        function_name = self.symbol_table.reverse_address(function_address)

        self.function_table.func_declare(function_name, function_address, "void")
        if function_name == "main":
            self.add_three_address_code(
                f"(JP, {self.i}, , )", index=1, increase_i=False
            )
            self.main_added = True

        self.function_table.func_declare(
            function_name, function_address, self.semantic_stack[-2]
        )  # it is void or int

        self.current_function_address = function_address

    def var(self, current_token: Token):
        var = self.semantic_stack.pop()
        var_type = self.semantic_stack.pop()
        self.add_three_address_code(f"(ASSIGN, #0, {var},)")

    def declare_global_arr(self, current_token: Token):
        size = int(self.semantic_stack.pop()[1:])  # remove # from int
        var = self.semantic_stack.pop()
        var_type = self.semantic_stack.pop()

        for i in range(size):
            self.add_three_address_code(f"(ASSIGN, #0, {var + i * 4})")

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
        if self.break_bool:
            if self.inside_if:
                self.add_three_address_code(f"(JP, @{self.semantic_stack[-7]}, , )")
                self.inside_if = False
            else:
                self.add_three_address_code(f"(JP, @{self.semantic_stack[-5]}, , )")
            self.break_bool = False
        else:
            print("semantic error No 'while' or 'switch'")
            pass
            ### todo (#lineno: Semantic Error! No 'while' or 'switch' found for 'break')

    def assign_to_func(self, current_token: Token):
        if not self.main_added:
            self.add_three_address_code(
                f"(ASSIGN, {self.semantic_stack[-1]}, {self.current_function_address}, )"
            )
            self.semantic_stack.pop()

    def set_array_address(self, current_token: Token):
        temp = self.symbol_table.get_temp()
        offset = self.semantic_stack.pop()
        base = self.semantic_stack.pop()

        self.add_three_address_code(f"(MULT, #4, {offset}, {temp})")
        self.add_three_address_code(f"(ADD, #{base}, @{temp}, {temp})")
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
            f"(JP, @{self.function_table.funcs[function_address]['address']}, , )"
        )
        self.add_three_address_code(f"(ASSIGN, {temp}, {self.retrun_temp},  )")

    def push_arg(self, current_token: Token):
        self.semantic_stack.append(
            self.function_table.funcs[self.func_call_stack[-1]]["params_address"][
                self.arg_counter
            ]
        )

    def if_start(self, current_token: Token):
        self.inside_if = True

    def end_function(self, current_token: Token):
        function_address = self.semantic_stack.pop()
        function_type = self.semantic_stack.pop()
        # maybe we should do something here
