import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton
from PyQt5.QtCore import Qt
from lexer import Lexer
from parser import Parser, SemanticError


class ParserApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("JSON Lexer and Parser")
        self.setGeometry(100, 100, 600, 400)

        # Layout
        layout = QVBoxLayout()

        # Input Label
        self.input_label = QLabel("Enter JSON-like string:", self)
        layout.addWidget(self.input_label)

        # Input Field (QTextEdit)
        self.input_text = QTextEdit(self)
        self.input_text.setPlaceholderText('{"name": "Bob", "age": 25, "height": 5.75, "active": true}')
        layout.addWidget(self.input_text)

        # Output Label
        self.output_label = QLabel("Parsed Output:", self)
        layout.addWidget(self.output_label)

        # Output Field (QTextEdit)
        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text)

        # Parse Button
        self.parse_button = QPushButton("Parse", self)
        self.parse_button.clicked.connect(self.parse_input)
        layout.addWidget(self.parse_button)

        # Set the layout to the window
        self.setLayout(layout)

    def parse_input(self):
        input_text = self.input_text.toPlainText().strip()  # Strip any extra spaces or line breaks
        lexer = Lexer(input_text)

        try:
            # Tokenize the input
            tokens = lexer.tokenize()

            # Parse with the shared recursive-descent parser (same rules as parser.py)
            parser = Parser(tokens)
            parsed_output = parser.parse()

            # Display the parsed output
            self.output_text.setPlainText(str(parsed_output))

        except SemanticError as se:
            # Handle semantic errors (e.g., invalid key names, invalid tokens, etc.)
            self.output_text.setPlainText(f"Semantic Error: {str(se)}")

        except SyntaxError as se:
            # Handle syntax errors (e.g., unexpected tokens, missing braces, etc.)
            self.output_text.setPlainText(f"Syntax Error: {str(se)}")

        except Exception as e:
            # Handle any other general errors
            self.output_text.setPlainText(f"Error: {str(e)}")


def main():
    app = QApplication(sys.argv)
    window = ParserApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
