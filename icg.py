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

    def code_gen(self, action_symbol, **kwargs):
        if action_symbol == "pid":
            self.pid(kwargs["input_addres"])

    def save_to_file(self):
        print(self.semantic_stack)
        write_three_address_codes_to_file(self.three_addres_codes)

    def pid(self, addres):
        self.semantic_stack.append(addres)
