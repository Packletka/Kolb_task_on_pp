import re
import json
import yaml
from bs4 import BeautifulSoup

class ArithmeticProcessor:
    def __init__(self, input_file, output_file, input_format, output_format):
        self.input_file = input_file
        self.output_file = output_file
        self.input_format = input_format
        self.output_format = output_format

    def read_from_file(self):
        with open(self.input_file, 'r') as file:
            if self.input_format == 'json':
                return json.load(file)
            elif self.input_format == 'yaml':
                return yaml.safe_load(file)
            elif self.input_format == 'text':
                return file.read()
            elif self.input_format == 'html':
                return file.read()

    def write_to_file(self, content):
        with open(self.output_file, 'w') as file:
            if self.output_format == 'json':
                json.dump(content, file)
            elif self.output_format == 'yaml':
                yaml.dump(content, file)
            elif self.output_format == 'text':
                file.write(content)
            elif self.output_format == 'html':
                file.write(content)

    def process_content(self, content):
        if self.input_format == 'html':
            soup = BeautifulSoup(content, 'html.parser')
            # Извлечь текст из HTML
            text = soup.get_text()
            processed_text = self.process_text(text)
            # Замена текста в HTML
            for elem in soup.find_all(string=True):
                if elem.strip():
                    elem.replace_with(self.process_text(elem))
            return str(soup)
        else:
            return self.process_text(content)

    def process_text(self, text):
        pattern = r'\d+\s*[\+\-\*\/]\s*\d+'
        return re.sub(pattern, self.evaluate_expression, text)

    def evaluate_expression(self, match):
        expression = match.group()
        result = eval(expression)
        return str(result)

    def run(self):
        content = self.read_from_file()
        processed_content = self.process_content(content)
        self.write_to_file(processed_content)


class ArithmeticProcessorBuilder:
    def __init__(self):
        self.input_file = None
        self.output_file = None
        self.input_format = None
        self.output_format = None

    def set_input_file(self, input_file):
        self.input_file = input_file
        return self

    def set_output_file(self, output_file):
        self.output_file = output_file
        return self

    def set_input_format(self, input_format):
        self.input_format = input_format
        return self

    def set_output_format(self, output_format):
        self.output_format = output_format
        return self

    def build(self):
        return ArithmeticProcessor(self.input_file, self.output_file, self.input_format, self.output_format)


def main():
    # Пример использования паттерна Builder
    builder = ArithmeticProcessorBuilder()
    processor = (builder
                 .set_input_file('input.html')
                 .set_output_file('output.html')
                 .set_input_format('text')
                 .set_output_format('text')
                 .build())

    processor.run()


if __name__ == "__main__":
    main()
