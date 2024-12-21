import re
import sys
import json

class ConfigToJSON:
    def __init__(self):
        self.variables = {}
        self.dictionaries = []
        self.errors = []

    def parse_file(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
        except FileNotFoundError:
            self.errors.append(f"Файл '{filepath}' не найден.")
            return

        # Удаляем комментарии
        content = re.sub(r'REM.*', '', content)  # Однострочные комментарии
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)  # Многострочные комментарии

        lines = content.splitlines()
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue

            try:
                if line.startswith("def"):
                    self.process_variable(line, line_num)
                elif line.startswith("table("):
                    self.process_dictionary(line, line_num)
                else:
                    self.errors.append(f"Строка {line_num}: неизвестный синтаксис '{line}'.")
            except Exception as e:
                self.errors.append(f"Строка {line_num}: ошибка парсинга: {e}")

    def process_variable(self, line, line_num):
        match = re.match(r'def\s+([_A-Za-z][_a-zA-Z0-9]*)\s*:=\s*(.+);', line)
        if match:
            name, expression = match.groups()
            value = self.evaluate_expression(expression, line_num)
            self.variables[name] = value
        else:
            self.errors.append(f"Строка {line_num}: некорректный синтаксис переменной.")

    def process_dictionary(self, line, line_num):
        match = re.match(r'table\((.+)\)', line, flags=re.DOTALL)
        if match:
            content = match.group(1)
            entries = re.findall(r'([_A-Za-z][_a-zA-Z0-9]*)\s*=>\s*([^,]+),?', content)
            if entries:
                dictionary = {}
                for key, value in entries:
                    dictionary[key] = self.evaluate_expression(value.strip(), line_num)
                self.dictionaries.append(dictionary)
            else:
                self.errors.append(f"Строка {line_num}: некорректный синтаксис словаря.")
        else:
            self.errors.append(f"Строка {line_num}: некорректный синтаксис table().")

    def evaluate_expression(self, expression, line_num):
        try:
            for var in self.variables:
                expression = re.sub(rf'\b{var}\b', str(self.variables[var]), expression)
            return eval(expression)
        except Exception as e:
            self.errors.append(f"Строка {line_num}: ошибка вычисления выражения '{expression}': {e}")
            return None

    def to_json(self):
        result = {
            "variables": self.variables,
            "dictionaries": self.dictionaries,
            "errors": self.errors,
        }
        return json.dumps(result, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python config_to_json.py <config_file>")
        sys.exit(1)

    config_file = sys.argv[1]

    parser = ConfigToJSON()
    parser.parse_file(config_file)
    print(parser.to_json())
