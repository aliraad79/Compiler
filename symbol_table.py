from typing import Dict, List
from utils import add_symbols_to_file


class SymbolTable:
    def __init__(self) -> None:
        self.table: Dict[str, int] = {}
        self.declared_symbols = []
        self.addres_pointer = 500

    def insert(self, lexeme: str) -> None:
        self.table[lexeme] = self.addres_pointer
        self.addres_pointer += 4

    def include(self, lexeme: str) -> bool:
        return lexeme in self.table.keys()

    def get_address(self, lexeme: str) -> int:
        return self.table[lexeme]

    def get_symbols(self) -> List[str]:
        return list(self.table.keys())

    def save_to_file(self) -> None:
        add_symbols_to_file(self.get_symbols())

    def get_temp(self) -> int:
        t = self.addres_pointer
        self.addres_pointer += 4
        return t

    def add_declared_symbols(self, lexeme) -> None:
        self.declared_symbols.append(lexeme)
