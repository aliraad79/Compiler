# Ali Ahmadi Kafeshani 97105703
# Mohamad Hosein Ghasemi 99011039

from scanner import Scanner
from parser import Parser
from icg import IntermidateCodeGenerator
from symbol_table import SymbolTable
import os

symbol_table = SymbolTable()
scanner = Scanner(symbol_table)
icg = IntermidateCodeGenerator(symbol_table, scanner)
parser = Parser(scanner, icg)
parser.start_parsing()
icg.save_to_file()
os.system("./tester_Linux.out > expected.txt")
