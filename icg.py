from symbol_table import SymbolTable
from utils import write_three_address_codes_to_file


class IntermidateCodeGenerator:
    def __init__(self, symbol_table: SymbolTable) -> None:
        self.semantic_stack = []
        self.three_addres_codes = {}
        self.i = 1

        self.symbol_table = symbol_table

    def code_gen(self, action_symbol, current_token_lexeme: str):
        if action_symbol == "pid":
            self.pid(current_token_lexeme)
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
        if action_symbol == "jp":
            self.jp()
        if action_symbol == "jpf_save":
            self.jpf_save()
        if action_symbol == "jpf":
            self.jpf()
        if action_symbol == "save":
            self.save()
        if action_symbol == "declare_id":
            self.declare_id(current_token_lexeme)
        if action_symbol == "parray":
            self.parray()

    def save_to_file(self):
        print(self.semantic_stack)
        write_three_address_codes_to_file(self.three_addres_codes)

    # Actions
    def pid(self, lexeme):
        if lexeme not in self.symbol_table.declared_symbols:
            print(f"Semantic error! not declared symbol : {lexeme}")
        self.semantic_stack.append(self.symbol_table.get_address(lexeme))

    def assign(self):
        src = self.semantic_stack.pop()
        dst = self.semantic_stack.pop()
        self.three_addres_codes[self.i] = f"(ASSIGN, {src}, {dst}, )"
        self.i += 1

    def pnum(self, number_lexeme: str):
        self.semantic_stack.append(f"#{number_lexeme}")

    def add_op(self, operand_lexeme: str):
        self.semantic_stack.append(operand_lexeme)

    def op(self):
        operand_map = {"+": "ADD", "-": "SUB", "*": "MULT", "<": "LT", "==": "EQ"}

        second_operand = self.semantic_stack.pop()
        operand = operand_map[self.semantic_stack.pop()]
        first_operand = self.semantic_stack.pop()

        tmp_address = self.symbol_table.get_temp()

        self.three_addres_codes[
            self.i
        ] = f"({operand}, {first_operand}, {second_operand}, {tmp_address})"

        self.i += 1
        self.semantic_stack.append(tmp_address)

    def label(self):
        self.semantic_stack.append(self.i)

    def until(self):
        condition = self.semantic_stack.pop()
        target = self.semantic_stack.pop()
        self.three_addres_codes[self.i] = f"(JPF, {condition}, {target}, )"
        self.i += 1

    def jp(self):
        pb_empty_place = self.semantic_stack.pop()
        self.three_addres_codes[pb_empty_place] = f"(JP, {self.i}, , )"

    def jpf_save(self):
        pb_empty_place = self.semantic_stack.pop()
        condition = self.semantic_stack.pop()
        self.three_addres_codes[pb_empty_place] = f"(JPF, {condition}, {self.i + 1}, )"

        self.semantic_stack.append(self.i)
        self.i += 1

    def jpf(self):
        pb_empty_place = self.semantic_stack.pop()
        condition = self.semantic_stack.pop()
        self.three_addres_codes[pb_empty_place] = (
            pb_empty_place,
            f"(JPF, {condition}, {self.i}, )",
        )

    def save(self):
        self.semantic_stack.append(self.i)
        self.i += 1

    def declare_id(self, lexeme):
        self.symbol_table.add_declared_symbols(lexeme)
        self.three_addres_codes[
            self.i
        ] = f"(ASSIGN, #0, {self.symbol_table.get_address(lexeme)}, )"
        self.i += 1

    def parray(self):
        ...
