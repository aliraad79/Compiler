from scanner import Token, TokenType
from symbol_table import SymbolTable
from utils import write_three_address_codes_to_file


class IntermidateCodeGenerator:
    def __init__(self, symbol_table: SymbolTable) -> None:
        self.semantic_stack = []
        self.three_addres_codes = {}
        self.i = 1

        self.symbol_table = symbol_table

        self.return_value = self.symbol_table.get_temp()
        self.return_address = self.symbol_table.get_temp()

        self.stack_pointer = self.symbol_table.get_temp()

    def code_gen(self, action_symbol, current_token: Token):
        print(self.semantic_stack, action_symbol, current_token.lexeme)

        if action_symbol == "padd":
            self.padd(current_token)
        if action_symbol == "assign":
            self.assign()
        if action_symbol == "op":
            self.op()
        if action_symbol == "label":
            self.label()
        if action_symbol == "until":
            self.until()
        if action_symbol == "jp":
            self.jp()
        if action_symbol == "jpf_save":
            self.jpf_save()
        if action_symbol == "jpf":
            self.jpf()
        if action_symbol == "save":
            self.save()
        if action_symbol == "declare_id":
            self.declare_id(current_token.lexeme)
        if action_symbol == "end":
            self.end()
        if action_symbol == "parray":
            self.parray()
        if action_symbol == "declare_arr":
            self.declare_arr()

        if action_symbol == "push_return_value":
            self.push_return_value()
        if action_symbol == "set_return_jump":
            self.set_return_jump()

    def save_to_file(self):
        print(self.semantic_stack)
        write_three_address_codes_to_file(self.three_addres_codes)

    def add_three_address_code(
        self, text: str, index: int = None, increase_i: bool = True
    ) -> None:
        self.three_addres_codes[index if index else self.i] = text
        self.i += 1 if increase_i else 0

    # Actions
    def padd(self, token: Token):
        if token.type == TokenType.ID.name:
            if token.lexeme not in self.symbol_table.declared_symbols:
                print(f"Semantic error! not declared symbol : {token.lexeme}")
            self.semantic_stack.append(self.symbol_table.get_address(token.lexeme))

        elif token.type == TokenType.NUM.name:
            self.semantic_stack.append(f"#{token.lexeme}")
        elif token.type == TokenType.SYMBOL.name:
            self.semantic_stack.append(token.lexeme)

    def assign(self):
        src = self.semantic_stack.pop()
        dst = self.semantic_stack[-1]
        self.add_three_address_code(f"(ASSIGN, {src}, {dst}, )")

    def op(self):
        operand_map = {"+": "ADD", "-": "SUB", "*": "MULT", "<": "LT", "==": "EQ"}

        second_operand = self.semantic_stack.pop()
        operand = operand_map[self.semantic_stack.pop()]
        first_operand = self.semantic_stack.pop()

        tmp_address = self.symbol_table.get_temp()

        self.add_three_address_code(
            f"({operand}, {first_operand}, {second_operand}, {tmp_address})"
        )

        self.semantic_stack.append(tmp_address)

    def label(self):
        self.semantic_stack.append(self.i)

    def until(self):
        condition = self.semantic_stack.pop()
        target = self.semantic_stack.pop()
        self.add_three_address_code(f"(JPF, {condition}, {target}, )")

    def jp(self):
        self.add_three_address_code(
            f"(JP, {self.i}, , )", index=self.semantic_stack.pop(), increase_i=False
        )

    def jpf_save(self):
        pb_empty_place = self.semantic_stack.pop()
        condition = self.semantic_stack.pop()
        self.add_three_address_code(
            text=f"(JPF, {condition}, {self.i + 1}, )",
            index=pb_empty_place,
            increase_i=False,
        )

        self.semantic_stack.append(self.i)
        self.i += 1

    def jpf(self):
        pb_empty_place = self.semantic_stack.pop()
        condition = self.semantic_stack.pop()
        self.add_three_address_code(
            text=f"(JPF, {condition}, {self.i}, )",
            index=pb_empty_place,
            increase_i=False,
        )

    def save(self):
        self.semantic_stack.append(self.i)
        self.i += 1

    def declare_id(self, lexeme):
        self.symbol_table.add_declared_symbols(lexeme)
        self.add_three_address_code(
            f"(ASSIGN, #0, {self.symbol_table.get_address(lexeme)}, )"
        )

    def end(self):
        self.semantic_stack.pop()

    def push_return_value(self):
        self.semantic_stack.append(self.return_value)

    def set_return_jump(self):
        self.add_three_address_code(f"(JP, @{self.return_address}, , )")

    def parray(self):
        array_index = self.semantic_stack.pop()
        temp = self.symbol_table.get_temp()
        self.add_three_address_code(f"(MULT, #4, {array_index}, {temp})")
        self.add_three_address_code(
            f"(ADD, {self.semantic_stack.pop()}, {temp}, {temp})"
        )
        self.semantic_stack.append(f"@{temp}")

    def declare_arr(self):
        self.add_three_address_code(
            f"(ASSIGN, {self.stack_pointer}, {self.semantic_stack[-2]}, )"
        )
        array_size = int(self.semantic_stack.pop()[1:])  # convert #NUM to NUM
        self.add_three_address_code(
            f"(ADD, #{4 * array_size}, {self.stack_pointer}, {self.stack_pointer})"
        )
