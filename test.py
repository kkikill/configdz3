import unittest
from io import StringIO
from config_to_json import ConfigToJSON

class TestConfigToJSON(unittest.TestCase):

    def setUp(self):
        self.parser = ConfigToJSON()

    def test_single_variable(self):
        config = """def x := 10;"""
        self.parser.parse_file(StringIO(config))
        result = self.parser.to_json()
        self.assertIn('"variables": {"x": 10}', result)
        self.assertNotIn('"errors": [', result)

    def test_single_table(self):
        config = """table(
            key1 => 100,
            key2 => 200
        );"""
        self.parser.parse_file(StringIO(config))
        result = self.parser.to_json()
        self.assertIn('"dictionaries": [', result)
        self.assertIn('{"key1": 100, "key2": 200}', result)
        self.assertNotIn('"errors": [', result)

    def test_variable_expression(self):
        config = """def x := 10; def y := x + 20;"""
        self.parser.parse_file(StringIO(config))
        result = self.parser.to_json()
        self.assertIn('"variables": {"x": 10, "y": 30}', result)
        self.assertNotIn('"errors": [', result)

    def test_table_with_expression(self):
        config = """def x := 50; table(
            key1 => x + 10,
            key2 => x * 2
        );"""
        self.parser.parse_file(StringIO(config))
        result = self.parser.to_json()
        self.assertIn('{"key1": 60, "key2": 100}', result)
        self.assertNotIn('"errors": [', result)

    def test_invalid_syntax(self):
        config = """def x = 10;"""
        self.parser.parse_file(StringIO(config))
        result = self.parser.to_json()
        self.assertIn('"errors": [', result)
        self.assertIn("некорректный синтаксис переменной", result)

    def test_missing_table_closing(self):
        config = """table(
            key1 => 100,
            key2 => 200"""
        self.parser.parse_file(StringIO(config))
        result = self.parser.to_json()
        self.assertIn('"errors": [', result)
        self.assertIn("некорректный синтаксис table()", result)

if __name__ == '__main__':
    unittest.main()
