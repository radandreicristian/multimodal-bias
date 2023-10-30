import unittest

from parameterized import parameterized

from src.caption.rule_modifier import RuleBasedModifier


class TestGenerator(unittest.TestCase):

    modifier = RuleBasedModifier()

    # 1 - nsubj
    # 2 - root
    # 4 - no noun nsubj + root is an adjective - invalid
    # 5 - no noun nsubj + root is a verb - invalid
    @parameterized.expand(
        [
            ("A little boy in kimono meditation before aikido competition in sports hall.", ("boy", 9)),
            ("A manager in the office.", ("manager", 2)),
            ("He is not a subject", (None, 0)),
            ("Going to a party", (None, 0)),
        ]
    )
    def test_subject_extraction(self, caption: str, expected_subject: str) -> None:
        actual_subject = self.modifier.get_subject(caption)
        self.assertEqual(actual_subject, expected_subject)

    # 1 - add adjectives as-is
    # 2 - add adjectives with correct capitalization
    # 3 - add adjectives with a/an correction
    # Todo 4 - Adjective order
    # Todo 5 - Duplicate adjectives
    @parameterized.expand(
        [
            ("A manager in the office", "young white", "A young white manager in the office"),
            ("Boy in kimono meditation", "asian", "Asian boy in kimono meditation"),
            ("A man doing pole dancing", "old asian", "An old asian man doing pole dancing"),
            ("A boa man doing nothing", "asian", "A boa asian man doing nothing"),
        ]
    )
    def test_insert_modifiers(self, caption: str, modifiers: str, expected_result):
        actual_result = self.modifier.modify(caption, modifiers)
        self.assertEqual(actual_result, expected_result)
