# Ali Ahmadi Kafeshani 97105703

from scanner import Scanner
from parser import Parser
from icg import IntermidateCodeGenerator
from symbol_table import SymbolTable
from function_table import FunctionTable

symbol_table = SymbolTable()
scanner = Scanner(symbol_table)
function_table = FunctionTable(scanner)
icg = IntermidateCodeGenerator(symbol_table, function_table)
parser = Parser(scanner, icg)
parser.start_parsing()
icg.save_to_file()
icg.run_output()
