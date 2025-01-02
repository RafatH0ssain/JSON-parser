import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton
from PyQt5.QtCore import Qt
from lexer import Lexer, TokenType, Token
from parser import Parser, ParseNode, SemanticError

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_pos = 0
        self.current_token = self.tokens[self.current_pos]

    def advance(self):
        self.current_pos += 1
        if self.current_pos < len(self.tokens):
            self.current_token = self.tokens[self.current_pos]
        else:
            self.current_token = Token(TokenType.EOF)

    def parse(self):
        # Start parsing based on the first token type
        if self.current_token.type == TokenType.LBRACE:
            return self.parse_object()  # Start parsing an object
        else:
            raise SyntaxError(f"Unexpected token type at the beginning: {self.current_token.type}")

    def parse_object(self):
        output = "Object:\n"
        self.advance()  # Skip the LBRACE

        # Check for empty objects
        if self.current_token.type == TokenType.RBRACE:
            self.advance()  # Skip the RBRACE for empty object
            return output

        while self.current_token.type != TokenType.EOF:
            output += self.parse_pair()

            if self.current_token.type == TokenType.RBRACE:
                self.advance()  # Skip RBRACE
                break
            elif self.current_token.type == TokenType.COMMA:
                self.advance()  # Skip COMMA
            else:
                raise SyntaxError(f"Expected ',' or '}}' but found {self.current_token.type}")

        return output

    def parse_pair(self):
        output = f"  Pair:\n"
        key_token = self.current_token

        if key_token.type != TokenType.STRING:
            raise SyntaxError(f"Expected a string key but found {key_token.type}")
        
        output += f"    Key: {key_token.type}: {key_token.value}\n"
        self.advance()  # Skip the key token

        if self.current_token.type != TokenType.COLON:
            raise SyntaxError(f"Expected ':' after key but found {self.current_token.type}")
        
        self.advance()  # Skip the COLON

        value_token = self.current_token
        if value_token.type in [TokenType.STRING, TokenType.NUMBER, TokenType.TRUE, TokenType.FALSE, TokenType.NULL]:
            output += f"    Value: {value_token.type}: {value_token.value}\n"
        else:
            raise SyntaxError(f"Unexpected value token type: {value_token.type}")
        
        self.advance()  # Skip the value token
        return output

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
        input_text = self.input_text.toPlainText()
        lexer = Lexer(input_text)

        try:
            # Tokenize the input
            tokens = lexer.tokenize()

            # Now parse the tokens
            parser = Parser(tokens)
            parsed_output = parser.parse()

            # Display the parsed output
            self.output_text.setPlainText(parsed_output)

        except SemanticError as se:
            # Handle semantic errors (e.g., invalid key names, invalid tokens, etc.)
            self.output_text.setPlainText(f"Semantic Error: {str(se)}")

        except SyntaxError as se:
            # Handle syntax errors (e.g., unexpected tokens, missing braces, etc.)
            self.output_text.setPlainText(f"Syntax Error: {str(se)}")

        except Exception as e:
            # Handle any other general errors
            self.output_text.setPlainText(f"Error: {str(e)}")

            input_text = self.input_text.toPlainText()
            lexer = Lexer(input_text)

            try:
                # Tokenize the input
                tokens = lexer.tokenize()

                # Now parse the tokens
                parser = Parser(tokens)
                parsed_output = parser.parse()

                # Display the parsed output
                self.output_text.setPlainText(str(parsed_output))

            except SemanticError as se:
                # Handle semantic errors (e.g., invalid key names, invalid tokens, etc.)
                self.output_text.setPlainText(f"Semantic Error: {str(se)}")

            except Exception as e:
                # Handle general errors (e.g., unexpected tokens, parsing errors, etc.)
                self.output_text.setPlainText(f"Error: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = ParserApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()