# Ali Ahmadi Kafeshani 97105703

from scanner import Scanner
from parser import Parser
from icg import IntermidateCodeGenerator
from symbol_table import SymbolTable
from function_table import FunctionTable
import os

symbol_table = SymbolTable()
scanner = Scanner(symbol_table)
function_table = FunctionTable(scanner, symbol_table)
icg = IntermidateCodeGenerator(symbol_table, function_table, scanner)
parser = Parser(scanner, icg)
parser.start_parsing()
icg.save_to_file()
# os.system("./tester_Linux.out")
