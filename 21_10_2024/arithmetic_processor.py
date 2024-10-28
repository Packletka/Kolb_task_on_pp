import re
import json
import yaml
from bs4 import BeautifulSoup
import sys

from PyQt5.QtWidgets import (
  QApplication,
  QWidget,
  QPushButton,
  QLabel,
  QLineEdit,
  QFileDialog,
  QVBoxLayout,
  QHBoxLayout,
  QTextEdit,
  QMessageBox
)

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

class ArithmeticProcessorUI(QWidget):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Арифметический процессор")

    self.input_file_label = QLabel("Входной файл:")
    self.input_file_edit = QLineEdit()
    self.input_file_button = QPushButton("Выбрать файл")
    self.input_file_button.clicked.connect(self.select_input_file)

    self.output_file_label = QLabel("Выходной файл:")
    self.output_file_edit = QLineEdit()
    self.output_file_button = QPushButton("Выбрать файл")
    self.output_file_button.clicked.connect(self.select_output_file)

    self.input_content_label = QLabel("Содержимое входного файла:")
    self.input_content_edit = QTextEdit()
    self.input_content_edit.setReadOnly(True)

    self.process_button = QPushButton("Обработать")
    self.process_button.clicked.connect(self.process_content)

    # Вертикальное расположение элементов
    main_layout = QVBoxLayout()

    # Расположение для input-файла
    input_file_layout = QHBoxLayout()
    input_file_layout.addWidget(self.input_file_label)
    input_file_layout.addWidget(self.input_file_edit)
    input_file_layout.addWidget(self.input_file_button)
    main_layout.addLayout(input_file_layout)

    # Расположение для output-файла
    output_file_layout = QHBoxLayout()
    output_file_layout.addWidget(self.output_file_label)
    output_file_layout.addWidget(self.output_file_edit)
    output_file_layout.addWidget(self.output_file_button)
    main_layout.addLayout(output_file_layout)

    # Расположение для отображения содержимого файла
    input_content_layout = QHBoxLayout()
    input_content_layout.addWidget(self.input_content_label)
    input_content_layout.addWidget(self.input_content_edit)
    main_layout.addLayout(input_content_layout)

    # Кнопка "Обработать"
    main_layout.addWidget(self.process_button)

    self.setLayout(main_layout)

  def select_input_file(self):
      file_name, _ = QFileDialog.getOpenFileName(self, "Выбрать входной файл", "", "Все файлы (*)")
      if file_name:
          self.input_file_edit.setText(file_name)
          self.load_input_content(file_name)

  def select_output_file(self):
      file_name, _ = QFileDialog.getSaveFileName(self, "Выбрать выходной файл", "", "Все файлы (*)")
      if file_name:
          self.output_file_edit.setText(file_name)

  def load_input_content(self, file_name):
      try:
          with open(file_name, 'r') as file:
              content = file.read()
              self.input_content_edit.setText(content)
      except Exception as e:
          QMessageBox.warning(self, "Ошибка", f"Не удалось открыть файл: {e}")

  def process_content(self):
      input_file = self.input_file_edit.text()
      output_file = self.output_file_edit.text()

      if not input_file or not output_file:
          QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите входной и выходной файлы.")
          return

      # ... (использовать ArithmeticProcessor для обработки) ...

      try:
          # Обработка данных и сохранение результата
          processor = ArithmeticProcessorBuilder()
          processor = processor.set_input_file(input_file) \
              .set_output_file(output_file) \
              .set_input_format('text') \
              .set_output_format('text') \
              .build()
          processor.run()
          QMessageBox.information(self, "Успех", "Обработка завершена.")
      except Exception as e:
          QMessageBox.warning(self, "Ошибка", f"Ошибка во время обработки: {e}")

if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = ArithmeticProcessorUI()  # Исправленный вызов класса
  window.show()
  sys.exit(app.exec_())
