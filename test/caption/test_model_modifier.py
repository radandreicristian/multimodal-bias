import unittest

from parameterized import parameterized

from src.caption.model_modifier import ModelBasedModifier


class TestGenerator(unittest.TestCase):

    modifier = ModelBasedModifier()

    # 1 - add adjectives as-is
    # 2 - add adjectives with correct capitalization
    # 3 - add adjectives with a/an correction
    # Todo 4 - Adjective order
    # Todo 5 - Duplicate adjectives
    @parameterized.expand(
        [
            ("A manager in the office.", "young white", "A young white manager in the office."),
            ("Boy in kimono doing meditation.", "asian", "Asian boy in kimono doing meditation."),
            ("A man doing pole dancing.", "old asian", "An old asian man doing pole dancing."),
        ]
    )
    def test_insert_modifiers(self, caption: str, modifiers: str, expected_result):
        actual_result = self.modifier.modify(caption, modifiers)
        self.assertEqual(actual_result, expected_result)
