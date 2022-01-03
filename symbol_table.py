from typing import Dict, List


class SymbolTable:
    def __init__(self) -> None:
        self.table: Dict[str, int] = {}
        self.addres_pointer = 100

    def insert(self, lexeme: str) -> None:
        self.table[lexeme] = self.addres_pointer
        self.addres_pointer += 4

    def include(self, lexeme: str) -> bool:
        return lexeme in self.table.keys()

    def get_address(self, lexeme: str) -> int:
        return self.table[lexeme]

    def get_symbols(self) -> List[str]:
        return list(self.table.keys())
