from tokens import TokenType, Token, KEYWORDS
from errors import LexerError

class Lexer:
    GENERAL_PURPOSE_REGISTERS = ['x9', 'x10', 'x11', 'x12', 'x13', 'x14', 'x15']

    def __init__(self, source_code):
        self.source_code = source_code
        self.position = 0
        self.line = 1

    def tokenize(self):
        tokens = []

        while self.position < len(self.source_code):
            char = self.source_code[self.position]

            if char == '\n':
                self.line += 1
                self.position += 1
                continue
            
            elif char == ' ':
                self.position += 1
                continue

            elif char.isalpha():
                word = self._read_word()
                token = self._classify_word(word)
                tokens.append(token)

            elif char.isdigit():
                number = self._read_number()
                tokens.append(Token(TokenType.INTEGER_VALUE, number, self.line))

            elif char == ":":
                tokens.append(Token(TokenType.COLON, ":", self.line))
                self.position += 1

            elif char == "@":
                tokens.append(Token(TokenType.AT, "@", self.line))
                self.position += 1

            elif char == "=":
                tokens.append(Token(TokenType.EQUALS, "=", self.line))
                self.position += 1

            elif char == "(":
                tokens.append(Token(TokenType.L_PAREN, "(", self.line))
                self.position += 1

            elif char == ")":
                tokens.append(Token(TokenType.R_PAREN, ")", self.line))
                self.position += 1

            else:
                raise LexerError(f"Unexpected character '{char}'", self.line)

        return tokens

    def _read_word(self):
        word = ''
        while self.position < len(self.source_code) and self.source_code[self.position].isalnum():
            word += self.source_code[self.position]
            self.position += 1
        return word

    def _read_number(self):
        number = ''
        while self.position < len(self.source_code) and self.source_code[self.position].isdigit():
            number += self.source_code[self.position]
            self.position += 1
        return number

    def _classify_word(self, word):
        if word in KEYWORDS:
            return Token(KEYWORDS[word], word, self.line)
        elif self._is_register(word):
            return Token(TokenType.REGISTER, word, self.line)
        else:
            return Token(TokenType.IDENTIFIER, word, self.line)

    def _is_register(self, word):
        return word in self.GENERAL_PURPOSE_REGISTERS