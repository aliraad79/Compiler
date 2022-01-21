from symbol_table import SymbolTable
from typing import List
from scanner import Scanner


class FunctionEntry:
    def __init__(self) -> None:
        self.params: List[str] = []
        self.params_type: List[str] = []
        self.params_address: List[str] = []
        self.params_array: List[str] = []


class FunctionTable:
    def __init__(self, scanner, symbol_table: SymbolTable):
        self.funcs = {}
        self.scanner: Scanner = scanner
        self.symbol_table: SymbolTable = symbol_table

    def func_declare(self, name, address, return_type):
        self.funcs[address] = {
            "name": name,
            "address": address,
            "return_type": return_type,
            "scope": self.symbol_table.scope_stack[-1],
            "line_num": self.scanner.line_number,
            "params": [],
            "params_type": [],
            "params_address": [],
            "params_array": [],
        }

    def add_param(self, func, param_name, param_type, param_address, is_array):
        self.funcs[func]["params"].append(param_name)
        self.funcs[func]["params_type"].append(param_type)
        self.funcs[func]["params_address"].append(param_address)
        self.funcs[func]["params_array"].append(is_array)
