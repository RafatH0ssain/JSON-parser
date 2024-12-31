import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton
from lexer import TokenType, Token
from PyQt5.QtCore import Qt

# Add your existing ParseNode and Parser classes here
class ParseNode:
    def __init__(self, node_type, value=None):
        self.node_type = node_type
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self, level=0):
        indent = " " * (level * 2)
        if self.node_type == "Object":
            result = f"{indent}Object:\n"
            for child in self.children:
                result += child.__repr__(level + 1)
        elif self.node_type == "Array":
            result = f"{indent}Array:\n"
            for child in self.children:
                result += child.__repr__(level + 1)
        elif self.node_type == "Pair":
            key_node = self.children[0]
            value_node = self.children[1]
            result = f"{indent}Pair:\n"
            result += f"{indent}  Key: {key_node.__repr__(level + 1)}\n"
            result += f"{indent}  Value: {value_node.__repr__(level + 1)}"
        elif self.node_type == "Key":
            result = f"{indent}Key: {self.value}"
        else:
            result = f"{indent}{self.node_type}: {self.value}"
        
        return result

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index]

    def get_next_token(self):
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = Token(TokenType.EOF)

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.get_next_token()
        else:
            raise Exception(f"Expected {token_type}, but got {self.current_token.type} at position {self.current_token_index}")

    def parse(self):
        return self.parse_value()

    def parse_value(self):
        token = self.current_token
        if token.type == TokenType.LBRACE:
            return self.parse_dict()
        elif token.type == TokenType.LBRACKET:
            return self.parse_list()
        elif token.type == TokenType.STRING:
            if token.value in ["true", "false"]:
                raise SemanticError(7, token, "Reserved keywords cannot be used as strings")
            self.eat(TokenType.STRING)
            return ParseNode("String", token.value)
        elif token.type == TokenType.NUMBER:
            if token.value.startswith("0") and len(token.value) > 1 and not token.value.startswith("0."):
                raise SemanticError(3, token, "Invalid Numbers: Leading zeros are not allowed.")
            if '.' in token.value and (token.value.startswith('.') or token.value.endswith('.')):
                raise SemanticError(1, token, "Invalid Decimal Numbers")
            self.eat(TokenType.NUMBER)
            return ParseNode("Number", token.value)
        elif token.type in [TokenType.TRUE, TokenType.FALSE, TokenType.NULL]:
            self.eat(token.type)
            return ParseNode(str(token.type), token.value)
        elif token.type == TokenType.EOF:
            raise Exception("Unexpected EOF while parsing value")
        else:
            raise Exception(f"Unexpected token {token.type} in value at position {self.current_token_index}")

    def parse_dict(self):
        node = ParseNode("Object")
        seen_keys = set()
        self.eat(TokenType.LBRACE)
        if self.current_token.type != TokenType.RBRACE:
            self.parse_pair(node, seen_keys)
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                if self.current_token.type != TokenType.STRING:
                    raise Exception(f"Unexpected token {self.current_token.type} in object at position {self.current_token_index}")
                self.parse_pair(node, seen_keys)
        self.eat(TokenType.RBRACE)
        
        return node

    def parse_pair(self, node, seen_keys):
        if self.current_token.type != TokenType.STRING:
            raise Exception(f"Expected key (STRING) but found {self.current_token.type} at position {self.current_token_index}")
        key_token = self.current_token

        if not key_token.value.strip():
            raise SemanticError(2, key_token, "Key cannot be empty")
        if key_token.value in ["true", "false"]:
            raise SemanticError(4, key_token, f"Reserved words '{key_token.value}' cannot be used as keys")
        if key_token.value in seen_keys:
            raise SemanticError(5, key_token, "Duplicate keys in dictionary")
        seen_keys.add(key_token.value)
        self.eat(TokenType.STRING)

        pair_node = ParseNode("Pair")
        key_node = ParseNode("Key", key_token.value)
        pair_node.add_child(key_node)

        if self.current_token.type != TokenType.COLON:
            raise Exception(f"Expected ':' but found {self.current_token.type} at position {self.current_token_index}")
        self.eat(TokenType.COLON)

        pair_node.add_child(self.parse_value())
        node.add_child(pair_node)

    def parse_list(self):
        node = ParseNode("Array")
        self.eat(TokenType.LBRACKET)
        if self.current_token.type != TokenType.RBRACKET:
            element_type = None
            first_element = self.parse_value()
            element_type = first_element.node_type
            node.add_child(first_element)
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                next_element = self.parse_value()
                if next_element.node_type != element_type:
                    raise SemanticError(6, next_element.value, "Inconsistent types in list elements")
                node.add_child(next_element)
        self.eat(TokenType.RBRACKET)
        
        return node

def parse_token_line(line):
    line = line.strip().strip("<>").split(", ", 1)
    
    if len(line) < 1:
        raise ValueError(f"Invalid token line format: {line}")
    
    token_type_str = line[0].strip()
    token_type = getattr(TokenType, token_type_str, None)  
    
    if token_type is None:
        raise ValueError(f"Invalid token type in line: {line}")
    
    token_value = line[1].strip() if len(line) > 1 else None
    
    return Token(token_type, token_value)

def parse_input_text(input_text):
    tokens = []
    lines = input_text.splitlines()
    for line in lines:
        token = parse_token_line(line)
        tokens.append(token)
    return tokens

def process_input(input_text):
    try:
        tokens = parse_input_text(input_text)
        parser = Parser(tokens)
        parse_tree = parser.parse()
        return str(parse_tree)
    except SemanticError as se:
        return str(se)
    except Exception as e:
        return f"Parsing Error: {e}"

def run_parser():
    input_text = text_input.toPlainText()  # Get the text from the QTextEdit widget
    result = process_input(input_text)
    text_output.setPlainText(result)  # Set the result in the output QTextEdit widget

# PyQt Setup
app = QApplication(sys.argv)

# Main Window
window = QWidget()
window.setWindowTitle("JSON Parser App")

# Layout
layout = QVBoxLayout()

# Input Textbox
text_input_label = QLabel("Enter Tokens:")
layout.addWidget(text_input_label)

text_input = QTextEdit()
text_input.setFixedHeight(150)
layout.addWidget(text_input)

# Output Textbox
text_output_label = QLabel("Parse Tree / Error Output:")
layout.addWidget(text_output_label)

text_output = QTextEdit()
text_output.setReadOnly(True)
text_output.setFixedHeight(250)
layout.addWidget(text_output)

# Parse Button
parse_button = QPushButton("Parse")
parse_button.clicked.connect(run_parser)
layout.addWidget(parse_button)

# Set the layout and show the window
window.setLayout(layout)
window.show()

sys.exit(app.exec_())