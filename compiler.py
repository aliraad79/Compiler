# Jafar Sadeghi 97106079
# Ali Ahmadi Kafeshani 97105703

from scanner import Scanner
from parser import Parser
from icg import IntermidateCodeGenerator

scanner = Scanner()
icg = IntermidateCodeGenerator()
parser = Parser(scanner, icg)
parser.start_parsing()
icg.save_to_file()
