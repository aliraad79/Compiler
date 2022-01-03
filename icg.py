from symbol_table import SymbolTable
from utils import write_three_address_codes_to_file


class IntermidateCodeGenerator:
    def __init__(self) -> None:
        self.semantic_stack = []
        self.three_addres_codes = []
        self.current_temp_memory_address = 500

    def get_temp(self):
        t = self.current_temp_memory_address
        self.current_temp_memory_address += 4
        return t

    def code_gen(
        self,
        action_symbol,
        current_token_lexeme: str,
        symbol_table: SymbolTable,
    ):
        if action_symbol == "pid":
            self.pid(symbol_table.get_address(current_token_lexeme))
        if action_symbol == "assign":
            self.assign()
        if action_symbol == "pnum":
            self.pnum(current_token_lexeme)
        if action_symbol == "add_op":
            self.add_op(current_token_lexeme)
        if action_symbol == "op":
            self.op()
        if action_symbol == "label":
            self.label()
        if action_symbol == "until":
            self.until()

    def save_to_file(self):
        print(self.semantic_stack)
        print(self.three_addres_codes)
        write_three_address_codes_to_file(self.three_addres_codes)

    # Actions
    def pid(self, addres):
        self.semantic_stack.append(addres)

    def assign(self):
        src = self.semantic_stack.pop()
        dst = self.semantic_stack.pop()
        self.three_addres_codes.append(f"(ASSIGN, {src}, {dst}, )")
        self.semantic_stack.append(dst)

    def pnum(self, number_lexeme: str):
        self.semantic_stack.append(f"#{number_lexeme}")

    def add_op(self, operand_lexeme: str):
        self.semantic_stack.append(operand_lexeme)

    def op(self):
        operand_map = {"+": "ADD", "-": "SUB", "*": "MULT", "<": "LT", "==": "EQ"}
        # print(self.semantic_stack)

        second_operand = self.semantic_stack.pop()
        operand = operand_map[self.semantic_stack.pop()]
        first_operand = self.semantic_stack.pop()

        tmp_address = self.get_temp()

        self.three_addres_codes.append(
            f"({operand}, {first_operand}, {second_operand}, {tmp_address})"
        )
        self.semantic_stack.append(tmp_address)

    def label(self):
        self.semantic_stack.append(len(self.three_addres_codes))

    def until(self):
        condition = self.semantic_stack.pop()
        target = self.semantic_stack.pop()
        self.three_addres_codes.append(f"(JPF, {condition}, {target}, )")
