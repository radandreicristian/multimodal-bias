import unittest

from parameterized import parameterized

from src.caption.mapper import map_age_to_attribute


class TestMapper(unittest.TestCase):
    @parameterized.expand([(25.0, "young"), (45.0, "middle-aged"), (80.0, "old")])
    def test_map_age_to_attribute(self, age: float, expected_attribute: str) -> None:
        actual_attribute = map_age_to_attribute(age)
        self.assertEqual(actual_attribute, expected_attribute)
