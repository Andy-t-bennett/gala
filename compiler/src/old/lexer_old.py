# First Stage of compiler used to read source file, break into tokens, and pass to parser

from tokens import TokenType, Token

class Lexer:
    KEYWORDS = {
        "int8": TokenType.INT8,
        "uint8": TokenType.UINT8,
        "bool": TokenType.BOOL,
        "char": TokenType.CHAR,
        "reg": TokenType.REG,
        "add": TokenType.ADD,
        "sub": TokenType.SUB,
        "true": TokenType.TRUE,
        "false": TokenType.FALSE,
        "stack": TokenType.STACK,
        "alloc": TokenType.ALLOC
    }

    def __init__(self, source_code):
        self.source_code = source_code
        self.position = 0

    def tokenize(self):
        tokens = []
        word = ''

        while self.position < len(self.source_code):
            char = self.source_code[self.position]

            if char == ' ':
                self.position +=  1
                continue
            
            elif char.isalpha():
                word = self._read_word()
                token = self._classify_word(word)
                tokens.append(token)

            elif char.isdigit():
                number = self._read_number()
                tokens.append(Token(TokenType.NUMBER, number))

            elif char == ":":
                tokens.append(Token(TokenType.COLON, ":"))
                self.position += 1

            elif char == "@":
                tokens.append(Token(TokenType.AT, "@"))
                self.position += 1

            elif char == "=":
                tokens.append(Token(TokenType.EQUALS, "="))
                self.position += 1

            elif char == "(":
                tokens.append(Token(TokenType.L_PAREN, "("))
                self.position += 1

            elif char == ")":
                tokens.append(Token(TokenType.R_PAREN, ")"))
                self.position += 1

            elif char == ",":
                tokens.append(Token(TokenType.COMA, ","))
                self.position += 1

            elif char == "'":
                character = self._read_character()
                tokens.append(Token(TokenType.CHARACTER, character))
            else:
                self.position += 1
        
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

    def _read_character(self):
        character = ''
        quote_count = 0
        while self.position < len(self.source_code) and quote_count < 2:
            if self.source_code[self.position] == "'":
                quote_count += 1
                self.position += 1
            else:
                character += self.source_code[self.position]
                self.position += 1

        return character   

    def _classify_word(self, word):
        if word in self.KEYWORDS:
            return Token(self.KEYWORDS[word], word)
        elif self._is_register(word):
            return Token(TokenType.REGISTER, word)
        else:
            return Token(TokenType.IDENTIFIER, word)

    def _is_register(self, word):
        general_purpose_regs = ['x9', 'x10', 'x11', 'x12', 'x13', 'x14', 'x15']
        if word in general_purpose_regs:
             return True
        else:
            return False



    