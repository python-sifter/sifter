# type: ignore

import os.path

import sifter.parser


def test_parser():
    in_filename = "parser_1.in"
    golden_filename = "parser_1.out"

    with open(os.path.join(os.path.dirname(__file__), in_filename), 'r', encoding='utf-8', newline='') as in_fh:
        test_output = str(sifter.parser.parse_file(in_fh))
    with open(os.path.join(os.path.dirname(__file__), golden_filename), 'r', encoding='utf-8', newline='') as golden_fh:
        golden_output = golden_fh.read()

    assert test_output == golden_output
