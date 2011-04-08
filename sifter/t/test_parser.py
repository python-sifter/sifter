import os.path
import unittest

import sifter.parser

class TestParseFile(unittest.TestCase):

    def test_files(self):
        for in_filename, golden_filename in (("parser_1.in", "parser_1.out"),):
            in_fh = open(os.path.join(os.path.dirname(__file__), in_filename))
            test_output = str(sifter.parser.parse_file(in_fh))
            in_fh.close()
            golden_fh = open(os.path.join(os.path.dirname(__file__),
                golden_filename))
            golden_output = golden_fh.read()
            golden_fh.close()
            self.assertEqual(test_output, golden_output)

if __name__ == '__main__':
    unittest.main()
