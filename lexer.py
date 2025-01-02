class TokenType:
    COMMA = 'COMMA'  # ','
    COLON = 'COLON'  # ':'
    LBRACE = 'LBRACE'  # '{'
    RBRACE = 'RBRACE'  # '}'
    LBRACKET = 'LBRACKET'  # '['
    RBRACKET = 'RBRACKET'  # ']'
    STRING = 'STRING'  # Tree leaves or node names
    NUMBER = 'NUMBER'  # Edge lengths or numeric values
    EOF = 'EOF'  # End of input
    TRUE = 'TRUE'  # true
    FALSE = 'FALSE'  # false
    NULL = 'NULL'  # null    

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value
        
    def __repr__(self):
        if self.value is not None:
            return f"<{self.type}, {self.value}>"
        return f"<{self.type}>"
    
# Lexer error
class LexerError(Exception):
    def __init__(self, position, character):
        self.position = position
        self.character = character
        super().__init__(f"Invalid character '{character}' at position {position}")
        
class Lexer:
    def __init__(self, input_text, output_widget=None):
        self.input_text = input_text
        self.tokens = []
        self.current_pos = 0
        self.current_char = input_text[0] if input_text else None
        self.output_widget = output_widget  # Store reference to the output widget
        self.brace_count = 0  # Initialize brace_count
        self.bracket_count = 0  # Initialize bracket_count
    
    def advance(self):
        self.current_pos += 1  # Fixed: it was 'self.position', which should be 'self.current_pos'
        if self.current_pos >= len(self.input_text):
            self.current_char = None
        else:
            self.current_char = self.input_text[self.current_pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def recognize_string(self):
        self.advance()
        result = ''
        while self.current_char is not None and self.current_char != '"':
            if self.current_char == '\\':
                self.advance()
                if self.current_char in ['"', '\\', 'n', 't', 'r']:
                    result += '\\' + self.current_char
                else:
                    raise LexerError(self.current_pos, self.current_char)  # Fixed: 'position' to 'current_pos'
            else:
                result += self.current_char
            self.advance()
        if self.current_char != '"':
            raise LexerError(self.current_pos, "Unclosed string literal")  # Fixed: 'position' to 'current_pos'
        self.advance()
        return Token(TokenType.STRING, result)
    
    def recognize_number(self):
        result = ''
        has_decimal = False
        has_exponent = False
        
        # Handle optional sign
        if self.current_char in ['-', '+']:
            result += self.current_char
            self.advance()
        
        # Handle digits before decimal or exponent
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        # Handle decimal point for floats
        if self.current_char == '.':
            has_decimal = True
            result += self.current_char
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()

        # Handle scientific notation (e or E)
        if self.current_char in ['e', 'E']:
            has_exponent = True
            result += self.current_char
            self.advance()
            if self.current_char in ['+', '-']:
                result += self.current_char
                self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()

        # If the number is improperly formatted, raise error
        if not result or (not result[0].isdigit() and result[0] not in ['-', '+']):
            raise LexerError(self.current_pos, "Invalid number format")

        if result.startswith("0") and len(result) > 1 and not has_decimal and not has_exponent:
            raise LexerError(self.current_pos, "Leading zeros not allowed for integers")
        
        return Token(TokenType.NUMBER, float(result) if has_decimal or has_exponent else int(result))

    def recognize_keyword(self):
        result = ''
        while self.current_char is not None and self.current_char.isalpha():
            result += self.current_char
            self.advance()
        if result == 'true':
            return Token(TokenType.TRUE)
        elif result == 'false':
            return Token(TokenType.FALSE)
        elif result == 'null':
            return Token(TokenType.NULL)
        else:
            raise LexerError(self.current_pos, f"Unexpected keyword '{result}'")

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char == '{':
                self.brace_count += 1  # Increment brace count
                self.advance()
                return Token(TokenType.LBRACE)
            if self.current_char == '}':
                if self.brace_count == 0:
                    raise LexerError(self.current_pos, "Unexpected closing brace")
                self.brace_count -= 1  # Decrement brace count
                self.advance()
                if self.current_char not in [None, ',', '}', ']']:
                    raise LexerError(self.current_pos, f"Unexpected character '{self.current_char}' after '}}'")
                return Token(TokenType.RBRACE)
            if self.current_char == '[':
                self.bracket_count += 1  # Increment bracket count
                self.advance()
                return Token(TokenType.LBRACKET)
            if self.current_char == ']':
                if self.bracket_count == 0:
                    raise LexerError(self.current_pos, "Unexpected closing bracket")
                self.bracket_count -= 1  # Decrement bracket count
                self.advance()
                if self.current_char not in [None, ',', '}', ']']:
                    raise LexerError(self.current_pos, f"Unexpected character '{self.current_char}' after ']'")
                return Token(TokenType.RBRACKET)
            if self.current_char == ',':
                self.advance()
                self.skip_whitespace()
                if self.current_char is None or self.current_char not in ['"', '{', '['] and not self.current_char.isalnum():
                    raise LexerError(self.current_pos, "Expected a value after ','")
                return Token(TokenType.COMMA)
            if self.current_char == ':':
                self.advance()
                self.skip_whitespace()
                if self.current_char is None or self.current_char not in ['"', '{', '['] and not self.current_char.isalnum():
                    raise LexerError(self.current_pos, "Expected a value after ':'")
                return Token(TokenType.COLON)
            if self.current_char == '"':
                return self.recognize_string()
            if self.current_char.isdigit() or self.current_char in ['-', '+']:
                return self.recognize_number()
            if self.current_char.isalpha():
                return self.recognize_keyword()
            raise LexerError(self.current_pos, f"Invalid character '{self.current_char}'")
        return Token(TokenType.EOF)

    # Tokenize the input
    def tokenize(self):
        tokens = []
        while True:
            try:
                token = self.get_next_token()
                if token.type == TokenType.EOF:
                    break
                tokens.append(token)
            except LexerError as e:
                self.display_error(f"Lexical Error: {e}")  # Send error to the output widget
                break
        tokens.append(Token(TokenType.EOF))  # Add EOF token at the end
        return tokens

    def display_error(self, error_message):
        if self.output_widget:
            current_text = self.output_widget.toPlainText()  # Get current content
            self.output_widget.setPlainText(current_text + "\n" + error_message)  # Append error message

# Testing the Lexer with input
if __name__ == "__main__":
    input_string = '{"name": "Bob", "age": 25, "height": 5.75, "active": true}'
    lexer = Lexer(input_string)
    try:
        tokens = lexer.tokenize()
        for token in tokens:
            print(token)
    except LexerError as e:
        print(f"Error: {e}")