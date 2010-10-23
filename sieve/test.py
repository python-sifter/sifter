from pprint import pprint
import sys

from parser import SieveLexer, SieveParser

parser = SieveParser()
rules = parser.parse(open(sys.argv[1]).read(), lexer=SieveLexer())
pprint(rules)

