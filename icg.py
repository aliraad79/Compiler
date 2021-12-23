from utils import write_three_address_codes_to_file


class IntermidateCodeGenerator:
    def __init__(self) -> None:
        self.semantic_stack = []
        self.three_addres_codes = []
        self.current_memory_address = 500

    def code_gen(self, action_symbol):
        ...

    def save_to_file(self):
        write_three_address_codes_to_file(self.three_addres_codes)
