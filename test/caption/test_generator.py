import unittest

from parameterized import parameterized

from src.caption.generator import CaptionGenerator


class TestGenerator(unittest.TestCase):

    generator = CaptionGenerator()

    @parameterized.expand(
        [
            ("A little boy in kimono meditation before aikido competition in sports hall.", "boy"),
            ("A manager in the office.", "manager"),
            ("A man is doing gardening", "man"),
        ]
    )
    def test_subject_extraction(self, caption: str, expected_subject: str) -> None:
        actual_subject = self.generator.get_subject(caption)
        self.assertEqual(actual_subject, expected_subject)
