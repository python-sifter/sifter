# type: ignore

import os.path
import unittest
import codecs

import sifter.parser


class TestParseFile(unittest.TestCase):

    def test_files(self) -> None:
        for in_filename, golden_filename in (("parser_1.in", "parser_1.out"),):
            with codecs.open(os.path.join(os.path.dirname(__file__), in_filename), encoding='utf-8') as in_fh:
                test_output = str(sifter.parser.parse_file(in_fh))
            with codecs.open(os.path.join(os.path.dirname(__file__), golden_filename),
                             encoding='utf-8') as golden_fh:
                golden_output = golden_fh.read()
            self.assertEqual(test_output, golden_output)


if __name__ == '__main__':
    unittest.main()
