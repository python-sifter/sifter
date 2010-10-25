import sys

import parser
rules = parser.parse_file(open(sys.argv[1]))
print(rules)
