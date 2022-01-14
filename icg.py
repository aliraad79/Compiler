import os
from scanner import Token, TokenType
from symbol_table import SymbolTable
from utils import write_three_address_codes_to_file


class IntermidateCodeGenerator:
    def __init__(self, symbol_table: SymbolTable) -> None:
        self.semantic_stack = []
        self.three_addres_codes = {}
        self.i = 0
        self.debug = True

        self.symbol_table = symbol_table

        self.init_icg_variables()
        self.add_output_function()

    def init_icg_variables(self) -> None:
        self.return_value = self.symbol_table.get_temp()
        self.add_three_address_code(f"(ASSIGN, #0, {self.return_value}, )")
        self.return_address = self.symbol_table.get_temp()
        self.add_three_address_code(f"(ASSIGN, #0, {self.return_address}, )")
        self.stack_pointer = self.symbol_table.get_temp()
        self.add_three_address_code(f"(ASSIGN, #0, {self.stack_pointer}, )")
        self.arg_pointer = []
        self.arg_pass_number = 0


    def add_output_function(self) -> None:
        self.symbol_table.insert("output", is_declred=True)
        # self.memory.program_block.append(f"(PRINT, {self.semantic_stack.pop()}, , )")

    def code_gen(self, action_symbol, current_token: Token):
        if self.debug:
            print(self.semantic_stack, action_symbol, current_token.lexeme)
        getattr(self, action_symbol)(current_token)

    def save_to_file(self):
        if self.debug:
            print("ss stack at the end : ", self.semantic_stack)
            print("Symbol table : ", self.symbol_table.table)
        write_three_address_codes_to_file(self.three_addres_codes)

    def run_output(self):
        os.system("./tester_Linux.out")

    def add_three_address_code(
        self, text: str, index: int = None, increase_i: bool = True
    ) -> None:
        self.three_addres_codes[index if index else self.i] = text
        self.i += 1 if increase_i else 0

    # Actions
    def padd(self, token: Token):
        if token.type == TokenType.ID.name:
            if token.lexeme not in self.symbol_table.get_declared_symbols():
                print(f"Semantic error! not declared symbol : {token.lexeme}")
            self.semantic_stack.append(self.symbol_table.get_address(token.lexeme))

        elif token.type == TokenType.NUM.name:
            self.semantic_stack.append(f"#{token.lexeme}")
        elif token.type == TokenType.SYMBOL.name:
            self.semantic_stack.append(token.lexeme)

    def assign(self, current_token:Token):
        src = self.semantic_stack.pop()
        dst = self.semantic_stack[-1]
        self.add_three_address_code(f"(ASSIGN, {src}, {dst}, )")

    def op(self, current_token:Token):
        operand_map = {"+": "ADD", "-": "SUB", "*": "MULT", "<": "LT", "==": "EQ"}

        second_operand = self.semantic_stack.pop()
        operand = operand_map[self.semantic_stack.pop()]
        first_operand = self.semantic_stack.pop()

        tmp_address = self.symbol_table.get_temp()

        self.add_three_address_code(
            f"({operand}, {first_operand}, {second_operand}, {tmp_address})"
        )

        self.semantic_stack.append(tmp_address)

    def label(self, current_token:Token):
        self.semantic_stack.append(self.i)

    def until(self, current_token:Token):
        condition = self.semantic_stack.pop()
        target = self.semantic_stack.pop()
        self.add_three_address_code(f"(JPF, {condition}, {target}, )")

    def jp(self, current_token:Token):
        self.add_three_address_code(
            f"(JP, {self.i}, , )", index=self.semantic_stack.pop(), increase_i=False
        )

    def jpf_save(self, current_token:Token):
        pb_empty_place = self.semantic_stack.pop()
        condition = self.semantic_stack.pop()
        self.add_three_address_code(
            text=f"(JPF, {condition}, {self.i + 1}, )",
            index=pb_empty_place,
            increase_i=False,
        )

        self.semantic_stack.append(self.i)
        self.i += 1

    def jpf(self, current_token:Token):
        pb_empty_place = self.semantic_stack.pop()
        condition = self.semantic_stack.pop()
        self.add_three_address_code(
            text=f"(JPF, {condition}, {self.i}, )",
            index=pb_empty_place,
            increase_i=False,
        )

    def save(self, current_token:Token):
        self.semantic_stack.append(self.i)
        self.i += 1

    def declare_id(self, current_token:Token):
        self.symbol_table.get_symbol_record(current_token.lexeme).make_declared()
        self.add_three_address_code(
            f"(ASSIGN, #0, {self.symbol_table.get_address(current_token.lexeme)}, )"
        )

    def end(self, current_token:Token):
        self.semantic_stack.pop()

    def push_return_value(self, current_token:Token):
        self.semantic_stack.append(self.return_value)

    def set_return_jump(self, current_token:Token):
        self.add_three_address_code(f"(JP, @{self.return_address}, , )")

    def parray(self, current_token:Token):
        array_index = self.semantic_stack.pop()
        temp = self.symbol_table.get_temp()
        self.add_three_address_code(f"(MULT, #4, {array_index}, {temp})")
        self.add_three_address_code(
            f"(ADD, {self.semantic_stack.pop()}, {temp}, {temp})"
        )
        self.semantic_stack.append(f"@{temp}")

    def declare_arr(self, current_token:Token):
        self.add_three_address_code(
            f"(ASSIGN, {self.stack_pointer}, {self.semantic_stack[-2]}, )"
        )
        array_size = int(self.semantic_stack.pop()[1:])  # convert #NUM to NUM
        self.add_three_address_code(
            f"(ADD, #{4 * array_size}, {self.stack_pointer}, {self.stack_pointer})"
        )
