import email
import os.path
import unittest
import codecs

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
            ("evaluation_3.msg", "evaluation_1.rules",
             [('redirect', 'field@example.com')]),
            ("evaluation_3.msg", "evaluation_2.rules",
             [('fileinto', ['INBOX'])]),
            ("evaluation_3.msg", "evaluation_3.rules",
             [('keep', None)]),
    )

    def setUp(self):
        self.messages = {}
        self.rules = {}
        for result in self.EVAL_RESULTS:
            with codecs.open(os.path.join(os.path.dirname(__file__), result[0]),
                             encoding='utf-8') as msg_fh:
                self.messages.setdefault(result[0], email.message_from_file(msg_fh))
            with codecs.open(os.path.join(os.path.dirname(__file__), result[1]),
                             encoding='utf-8') as rule_fh:
                self.rules.setdefault(result[1], sifter.parser.parse_file(rule_fh))

    def test_msg_rule_cross_product(self):
        for result in self.EVAL_RESULTS:
            self.assertEqual(
                self.rules[result[1]].evaluate(self.messages[result[0]]),
                result[2]
                )

if __name__ == '__main__':
    unittest.main()
