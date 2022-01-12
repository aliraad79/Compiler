# Ali Ahmadi Kafeshani 97105703

from scanner import Scanner
from parser import Parser
from icg import IntermidateCodeGenerator
from symbol_table import SymbolTable

symbol_table = SymbolTable()
scanner = Scanner(symbol_table)
icg = IntermidateCodeGenerator(symbol_table)
parser = Parser(scanner, icg)
parser.start_parsing()
icg.save_to_file()
icg.run_output()
