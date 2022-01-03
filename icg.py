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

    def save_to_file(self):
        print(self.semantic_stack)
        print(self.three_addres_codes)
        write_three_address_codes_to_file(self.three_addres_codes)

    def pid(self, addres):
        self.semantic_stack.append(addres)

    def assign(self):
        src = self.semantic_stack.pop()
        dst = self.semantic_stack.pop()
        self.three_addres_codes.append(f"(ASSIGN, {src}, {dst}, )")
        self.semantic_stack.append(dst)
