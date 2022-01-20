from typing import Dict, List
from utils import add_symbols_to_file
from enum import Enum


class SymbolTableRowType(Enum):
    int = 1
    void = 2
    array = 3
    none = 4


class FuncOrVar(Enum):
    func = 1
    var = 2


class SymbolTableRow:
    def __init__(
        self,
        lexeme: str,
        scope: int,
        address: int,
        _type: SymbolTableRowType = SymbolTableRowType.none,
        is_declred: bool = False,
        func_or_var: FuncOrVar = FuncOrVar.var,
    ) -> None:
        self.lexeme = lexeme
        self.is_declred = is_declred
        self.type = _type
        self.scope = scope
        self.address = address
        self.func_or_var = func_or_var

        self.param_types: List[str] = []
        self.param_is_array: List[bool] = []
        self.param_number: int = 0

    def make_declared(self):
        self.is_declred = True

    def __contains__(self, other):
        return other == self.lexeme

    def __eq__(self, __o: object) -> bool:
        return __o == self.lexeme

    def __repr__(self) -> str:
        return f"{self.lexeme}:{self.address}:{self.scope}:{self.type.name}"


class SymbolTable:
    def __init__(self) -> None:
        self.table: List[SymbolTableRow] = []
        self.addres_pointer = 500
        self.scope_stack = [0]

    def insert(self, lexeme: str, is_declred: bool = False) -> None:
        self.table.append(
            SymbolTableRow(
                lexeme, self.scope_stack[-1], self.addres_pointer, is_declred=is_declred
            )
        )
        self.addres_pointer += 4
        return self.addres_pointer - 4

    def include(self, lexeme: str) -> bool:
        return lexeme in self.table

    def get_address(self, lexeme: str) -> int:
        for i in self.table[::-1]:
            if i.lexeme == lexeme:
                return i.address

    def get_row(self, lexeme: str) -> SymbolTableRow:
        for i in self.table[::-1]:
            if i.lexeme == lexeme:
                return i

    def reverse_address(self, address: int) -> SymbolTableRow:
        for i in self.table[::-1]:
            if i.address == address:
                return i

    def get_rows(self) -> List[SymbolTableRow]:
        return [i for i in self.table]

    def get_temp(self) -> int:
        t = self.addres_pointer
        self.addres_pointer += 4
        return t

    def save_to_file(self) -> None:
        add_symbols_to_file([i.lexeme for i in self.table])
