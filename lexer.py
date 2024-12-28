
# Token types
class TokenType:
    COMMA = 'COMMA' # ','
    COLON = 'COLON' # ':'
    LBRACE = 'LBRACE' # '{'
    RBRACE = 'RBRACE' # '}'
    LBRACKET = 'LBRACKET' # '['
    RBRACKET = 'RBRACKET' # ']'
    STRING = 'STRING' # Tree leaves or node names
    NUMBER = 'NUMBER' # Edge lengths or numeric values
    EOF = 'EOF' # End of input
    TRUE = 'TRUE' # true
    FALSE = 'FALSE' # false
    NULL = 'NULL' # null    

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
    def __init__(self, input_text):
        self.input_text = input_text
        self.position = 0
        self.current_char = self.input_text[self.position] if self.input_text else None
        self.brace_count = 0
        self.bracket_count = 0
    
    def advance(self):
        self.position += 1
        if self.position >= len(self.input_text):
            self.current_char = None
        else:
            self.current_char = self.input_text[self.position]

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
                    raise LexerError(self.position, self.current_char)
            else:
                result += self.current_char
            self.advance()
        if self.current_char != '"':
            raise LexerError(self.position, "Unclosed string literal")
        self.advance()
        return Token(TokenType.STRING, result)
    
    def recognize_number(self):
        result = ''
        while self.current_char is not None and (
            self.current_char.isdigit() or self.current_char in
            ['.', 'e', 'E', '-', '+']):
            result += self.current_char
            self.advance()
        return Token(TokenType.NUMBER, float(result))

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
            raise LexerError(self.position, f"Unexpected keyword '{result}'")

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char == '{':
                self.brace_count += 1
                self.advance()
                return Token(TokenType.LBRACE)
            if self.current_char == '}':
                if self.brace_count == 0:
                    raise LexerError(self.position, "Unexpected closing brace")
                self.brace_count -= 1
                self.advance()
                if self.current_char not in [None, ',', '}', ']']:
                    raise LexerError(self.position, f"Unexpected character '{self.current_char}' after '}}'")
                return Token(TokenType.RBRACE)
            if self.current_char == '[':
                self.bracket_count += 1
                self.advance()
                return Token(TokenType.LBRACKET)
            if self.current_char == ']':
                if self.bracket_count == 0:
                    raise LexerError(self.position, "Unexpected closing bracket")
                self.bracket_count -= 1
                self.advance()
                if self.current_char not in [None, ',', '}', ']']:
                    raise LexerError(self.position, f"Unexpected character '{self.current_char}' after ']'")
                return Token(TokenType.RBRACKET)
            if self.current_char == ',':
                self.advance()
                self.skip_whitespace()
                if self.current_char is None or self.current_char not in ['"', '{', '['] and not self.current_char.isalnum():
                    raise LexerError(self.position, "Expected a value after ','")
                return Token(TokenType.COMMA)
            if self.current_char == ':':
                self.advance()
                self.skip_whitespace()
                if self.current_char is None or self.current_char not in ['"', '{', '['] and not self.current_char.isalnum():
                    raise LexerError(self.position, "Expected a value after ':'")
                return Token(TokenType.COLON)
            if self.current_char == '"':
                return self.recognize_string()
            if self.current_char.isdigit() or self.current_char in ['-', '+']:
                return self.recognize_number()
            if self.current_char.isalpha():
                return self.recognize_keyword()
            raise LexerError(self.position, f"Invalid character '{self.current_char}'")
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
                print(f"Lexical Error: {e}")
                break
            # tokens.append(token)

        if self.brace_count != 0:
            raise LexerError(self.position, "Unclosed brace")
        if self.bracket_count != 0:
            raise LexerError(self.position, "Unclosed bracket")
            
        return tokens
    
# Testing the Lexer with input
if __name__ == "__main__":
    input_string = '{"name": "Bob", "age": 25}'
    lexer = Lexer(input_string)
    try:
        tokens = lexer.tokenize()
        for token in tokens:
            print(token)
    except LexerError as e:
        print(f"Error: {e}")
