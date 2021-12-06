# Jafar Sadeghi 97106079
# Ali Ahmadi Kafeshani 97105703

from scanner import Scanner
from parser import Parser

scanner = Scanner()
parser = Parser(scanner)
parser.start()
parser.save_to_file()