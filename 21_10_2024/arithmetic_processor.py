import re
import json
import yaml
import xml.etree.ElementTree as ET
import input_files.arithmetic_pb2 as protobuf
from bs4 import BeautifulSoup
import sys
import os
import zipfile
from cryptography.fernet import Fernet

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QDesktopWidget,
    QPushButton,
    QLabel,
    QLineEdit,
    QFileDialog,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QMessageBox,
    QDialog,
    QRadioButton
)


class ArithmeticProcessor:
    def __init__(self, input_file, output_file, input_format, output_format):
        self.input_file = input_file
        self.output_file = output_file
        self.input_format = input_format
        self.output_format = output_format

    def read_from_file(self):
        with open(self.input_file, 'rb') as file:
            if self.input_format == 'json':
                return json.load(file)
            elif self.input_format == 'yaml':
                return yaml.safe_load(file)
            elif self.input_format in ('text', 'html'):
                return file.read().decode('utf-8')
            elif self.input_format == 'xml':
                return self.read_xml(file)
            elif self.input_format == 'protobuf':
                return self.read_protobuf(file)

    def read_protobuf(self, file):
        data = protobuf.ArithmeticData()
        data.ParseFromString(file.read())
        return data.content

    def read_xml(self, file):
        tree = ET.parse(file)
        root = tree.getroot()
        return self.xml_to_text(root)

    def xml_to_text(self, element):
        text = [element.text or ""]
        for child in element:
            text.append(self.xml_to_text(child))
        return " ".join(text)

    def write_to_file(self, content):
        with open(self.output_file, 'wb') as file:
            if self.output_format == 'json':
                json.dump(content, file)
            elif self.output_format == 'yaml':
                yaml.dump(content, file)
            elif self.output_format in ('text', 'html'):
                file.write(content.encode('utf-8'))
            elif self.output_format == 'xml':
                self.write_xml(content, file)
            elif self.output_format == 'protobuf':
                self.write_protobuf(content, file)

    def write_protobuf(self, content, file):
        data = protobuf.ArithmeticData()
        data.content = content
        file.write(data.SerializeToString())

    def write_xml(self, content, file):
        root = ET.Element("ProcessedContent")
        ET.SubElement(root, "Result").text = content
        tree = ET.ElementTree(root)
        tree.write(file)

    def process_content(self, content):
        if self.input_format == 'html':
            soup = BeautifulSoup(content, 'html.parser')
            text = soup.get_text()
            processed_text = self.process_text(text)
            for elem in soup.find_all(string=True):
                if elem.strip():
                    elem.replace_with(self.process_text(elem))
            return str(soup)
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
        self.setWindowTitle("UI для сквозной задачи")

        # UI Elements Initialization
        self.init_ui_elements()
        self.layout_ui_elements()

        # Center the window on the screen
        self.center()

    def center(self):
        # Get the screen geometry
        screen = QDesktopWidget().screenGeometry()
        # Get the window geometry
        size = self.geometry()
        # Calculate the new position
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)  # Move the window to the center

    def init_ui_elements(self):
        self.action_label = QLabel("Производить ли действия над input-файлом?")
        self.radio_yes = QRadioButton("Да")
        self.radio_no = QRadioButton("Нет")
        self.radio_no.setChecked(True)

        self.input_file_edit = QLineEdit()
        self.input_file_button = QPushButton("Выбрать файл")
        self.input_file_button.clicked.connect(self.select_input_file)

        self.output_file_edit = QLineEdit()
        self.output_file_button = QPushButton("Выбрать файл")
        self.output_file_button.clicked.connect(self.select_output_file)

        self.input_content_edit = QTextEdit()
        self.input_content_edit.setReadOnly(True)

        self.process_button = QPushButton("Обработать")
        self.reverse_process_button = QPushButton("Обратное действие -> Обработать")
        self.process_button.hide()
        self.reverse_process_button.hide()

        # Connect the process button to the new method
        self.process_button.clicked.connect(self.process_content)
        self.reverse_process_button.clicked.connect(self.reverse_action)
        self.exit_button = QPushButton("Выход")
        self.exit_button.clicked.connect(self.close)

    def layout_ui_elements(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.action_label)
        main_layout.addWidget(self.radio_yes)
        main_layout.addWidget(self.radio_no)

        input_file_layout = QHBoxLayout()
        input_file_layout.addWidget(QLabel("Входной файл:"))
        input_file_layout.addWidget(self.input_file_edit)
        input_file_layout.addWidget(self.input_file_button)
        main_layout.addLayout(input_file_layout)

        output_file_layout = QHBoxLayout()
        output_file_layout.addWidget(QLabel("Выходной файл:"))
        output_file_layout.addWidget(self.output_file_edit)
        output_file_layout.addWidget(self.output_file_button)
        main_layout.addLayout(output_file_layout)

        input_content_layout = QHBoxLayout()
        input_content_layout.addWidget(QLabel("Содержимое входного файла:"))
        input_content_layout.addWidget(self.input_content_edit)
        main_layout.addLayout(input_content_layout)

        main_layout.addWidget(self.reverse_process_button)
        main_layout.addWidget(self.process_button)
        main_layout.addWidget(self.exit_button)

        self.setLayout(main_layout)

    def select_input_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Выбрать входной файл", "", "Все файлы (*)")
        if file_name:
            self.input_file_edit.setText(file_name)
            self.load_input_content(file_name)
            self.update_process_buttons()
            if self.radio_yes.isChecked():
                self.show_action_options(file_name)

    def select_output_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Выбрать выходной файл", "", "Все файлы (*)")
        if file_name:
            self.output_file_edit.setText(file_name)
            self.update_process_buttons()

    def update_process_buttons(self):
        input_file_selected = bool(self.input_file_edit.text())
        output_file_selected = bool(self.output_file_edit.text())

        if input_file_selected and output_file_selected:
            if self.input_file_edit.text().endswith(('.encrypted', '.decrypted')):
                self.reverse_process_button.show()
                self.process_button.hide()
            else:
                self.reverse_process_button.hide()
                self.process_button.show()
        else:
            self.process_button.hide()
            self.reverse_process_button.hide()

    def show_action_options(self, input_file):
        self.options_dialog = QDialog(self)
        self.options_dialog.setWindowTitle("Выбор опций")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Выберите опцию:"))

        self.encrypt_radio = QRadioButton("Зашифровать")
        self.archive_radio = QRadioButton("Архивировать")
        self.encrypt_then_archive_radio = QRadioButton("Зашифровать, потом Архивировать")
        self.archive_then_encrypt_radio = QRadioButton("Архивировать, потом Зашифровать")

        layout.addWidget(self.encrypt_radio)
        layout.addWidget(self.archive_radio)
        layout.addWidget(self.encrypt_then_archive_radio)
        layout.addWidget(self.archive_then_encrypt_radio)

        confirm_button = QPushButton("Подтвердить")
        confirm_button.clicked.connect(lambda: self.handle_action_options(self.options_dialog, input_file))
        layout.addWidget(confirm_button)

        self.options_dialog.setLayout(layout)
        self.options_dialog.exec_()

    def handle_action_options(self, dialog, input_file):
        if not (self.encrypt_radio.isChecked() or self.archive_radio.isChecked() or
                self.encrypt_then_archive_radio.isChecked() or self.archive_then_encrypt_radio.isChecked()):
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, выберите хотя бы одну опцию.")
            return

        try:
            if self.encrypt_radio.isChecked():
                encrypted_file = self.encrypt_file(input_file)
                self.input_file_edit.setText(encrypted_file)
                QMessageBox.information(self, "Успех", "Файл успешно зашифрован.")
            elif self.archive_radio.isChecked():
                archived_file = self.archive_file(input_file)
                self.input_file_edit.setText(archived_file)
                QMessageBox.information(self, "Успех", "Файл успешно архивирован.")
            elif self.encrypt_then_archive_radio.isChecked():
                encrypted_file = self.encrypt_file(input_file)
                archived_file = self.archive_file(encrypted_file)
                self.input_file_edit.setText(archived_file)
                QMessageBox.information(self, "Успех", "Файл успешно зашифрован и архивирован.")
            elif self.archive_then_encrypt_radio.isChecked():
                archived_file = self.archive_file(input_file)
                encrypted_file = self.encrypt_file(archived_file)
                self.input_file_edit.setText(encrypted_file)
                QMessageBox.information(self, "Успех", "Файл успешно архивирован и зашифрован.")

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")

        dialog.accept()

    def encrypt_file(self, input_file):
        key = Fernet.generate_key()
        cipher = Fernet(key)

        # Сохранение ключа в файл
        key_file_name = input_file + '.key'
        with open(key_file_name, 'wb') as key_file:
            key_file.write(key)

        with open(input_file, 'rb') as file:
            original_data = file.read()
        encrypted_data = cipher.encrypt(original_data)
        encrypted_file_name = input_file + '.encrypted'
        with open(encrypted_file_name, 'wb') as enc_file:
            enc_file.write(encrypted_data)

        return encrypted_file_name

    def archive_file(self, input_file):
        archive_file_name = input_file + '.zip'
        with zipfile.ZipFile(archive_file_name, 'w') as zipf:
            zipf.write(input_file, os.path.basename(input_file))
        return archive_file_name

    def load_input_content(self, file_name):
        try:
            with open(file_name, 'rb') as file:
                content = file.read()
                self.input_content_edit.setText(content.decode('utf-8', 'ignore'))
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось открыть файл: {e}")

    def process_content(self):
        input_file = self.input_file_edit.text()
        output_file = self.output_file_edit.text()

        if not input_file or not output_file:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите входной файл и выходной файл.")
            return

        # Determine the input format based on file extension (you may want to improve this logic)
        if input_file.endswith('.json'):
            input_format = 'json'
        elif input_file.endswith('.yaml'):
            input_format = 'yaml'
        elif input_file.endswith('.xml'):
            input_format = 'xml'
        elif input_file.endswith('.html'):
            input_format = 'html'
        elif input_file.endswith('.txt'):
            input_format = 'text'
        elif input_file.endswith('.encrypted'):
            # Handle encrypted files appropriately if needed
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, расшифруйте файл перед обработкой.")
            return
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный формат входного файла.")
            return

        # Create an instance of the ArithmeticProcessor
        processor = ArithmeticProcessor(input_file, output_file, input_format, 'text')  # Set output format as needed

        try:
            processor.run()  # This will read, process, and write the output
            QMessageBox.information(self, "Успех", "Файл успешно обработан.")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка при обработке файла: {e}")

    def reverse_action(self):
        input_file = self.input_file_edit.text()
        if not input_file:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите файл для обратного действия.")
            return

        try:
            if input_file.endswith('.encrypted'):
                decrypted_file = self.decrypt_file(input_file)
                if decrypted_file:  # Проверяем, что расшифровка прошла успешно
                    self.input_file_edit.setText(decrypted_file)
                    QMessageBox.information(self, "Успех", "Файл успешно расшифрован.")
            elif input_file.endswith('.zip'):
                extracted_files = self.extract_file(input_file)
                for file in extracted_files:
                    self.process_content(file)  # Обрабатываем каждый извлечённый файл
                QMessageBox.information(self, "Успех", "Файлы успешно извлечены и обработаны.")
            else:
                QMessageBox.warning(self, "Ошибка", "Файл не является зашифрованным или архивированным.")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка при выполнении обратного действия: {e}")

    def decrypt_file(self, input_file):
        try:
            # Загрузка ключа из файла
            key_file_name = input_file.replace('.encrypted', '.key')
            with open(key_file_name, 'rb') as key_file:
                key = key_file.read()

            cipher = Fernet(key)
            with open(input_file, 'rb') as file:
                encrypted_data = file.read()

            decrypted_data = cipher.decrypt(encrypted_data)

            output_file = self.output_file_edit.text() or input_file.replace('.encrypted', '.decrypted')

            with open(output_file, 'wb') as dec_file:
                dec_file.write(decrypted_data)

            return output_file
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка при расшифровке файла: {e}")
            return None

    def extract_file(self, input_file):
        extracted_files = []
        try:
            output_dir = QFileDialog.getExistingDirectory(self, "Выбрать папку для извлечения")
            if output_dir:
                with zipfile.ZipFile(input_file, 'r') as zip_ref:
                    zip_ref.extractall(output_dir)
                    extracted_files = zip_ref.namelist()  # Get list of extracted files
                return [os.path.join(output_dir, f) for f in extracted_files]
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка при извлечении файла: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ArithmeticProcessorUI()
    window.show()
    sys.exit(app.exec_())
