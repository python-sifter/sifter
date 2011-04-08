import email
import os.path
import unittest

import sifter.parser

class TestEvaluateRules(unittest.TestCase):

    EVAL_RESULTS = (
            ("evaluation_1.msg", "evaluation_1.rules",
             [('redirect', 'acm@example.com')]),
            ("evaluation_1.msg", "evaluation_2.rules",
             []),
            ("evaluation_2.msg", "evaluation_1.rules",
             [('redirect', 'postmaster@example.com')]),
            ("evaluation_2.msg", "evaluation_2.rules",
             []),
    )

    def setUp(self):
        self.messages = {}
        self.rules = {}
        for result in self.EVAL_RESULTS:
            msg_fh = open(os.path.join(os.path.dirname(__file__), result[0]))
            self.messages.setdefault(result[0], email.message_from_file(msg_fh))
            msg_fh.close()
            rule_fh = open(os.path.join(os.path.dirname(__file__), result[1]))
            self.rules.setdefault(result[1], sifter.parser.parse_file(rule_fh))
            rule_fh.close()

    def test_msg_rule_cross_product(self):
        for result in self.EVAL_RESULTS:
            self.assertEqual(
                self.rules[result[1]].evaluate(self.messages[result[0]]),
                result[2]
                )

if __name__ == '__main__':
    unittest.main()
