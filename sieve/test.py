import sys

import sieve.parser
rules = sieve.parser.parse_file(open(sys.argv[1]))
print(rules)
