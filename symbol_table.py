class SymbolTable:
    def __init__(self) -> None:
        self.table = {}
        self.addres_pointer = 100

    def insert(self, lexeme):
        self.table[lexeme] = self.addres_pointer

    def include(self, lexeme):
        return lexeme in self.table.keys()

    def get_symbols(self):
        return list(self.table.keys())