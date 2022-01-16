from typing import List
from scanner import Scanner


class FunctionEntry:
    def __init__(self) -> None:
        self.params: List[str] = []
        self.params_type: List[str] = []
        self.params_address: List[str] = []
        self.params_array: List[str] = []


class FunctionTable:
    def __init__(self, scanner):
        self.funcs = {}
        self.params = {}
        self.scanner: Scanner = scanner

    def func_declare(self, name, address, return_type):
        self.funcs[address] = {
            "name": name,
            "address": address,
            "return_type": return_type,
            "symbol_table": {},
            # "scope": scope_stack.top(),
            "line_num": self.scanner.line_number,
            "params": [],
            "params_type": [],
            "params_address": [],
            "params_array": [],
            "return_addresses": [],
        }

    def add_param(self, func, param_name, param_type, param_address, is_array):
        self.funcs[func]["params"].append(param_name)
        self.funcs[func]["params_type"].append(param_type)
        self.funcs[func]["params_address"].append(param_address)
        self.funcs[func]["params_array"].append(is_array)

    def get_function_name(self, address):
        return self.funcs[address]["name"]

    def get_function_address(self, name):
        for ad, value in self.funcs.items():
            if name == value["name"]:
                return ad
        print("Error")

    def get_parameter(self, func_name, param_name):
        return self.params.get(func_name + "_" + param_name)
