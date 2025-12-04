class TokenType():
    # Keywords
    REG = "REG"
    INT8 = "INT8"

    # Values
    REGISTER = "REGISTER"
    IDENTIFIER = "IDENTIFIER"
    INTEGER_VALUE = "INTEGER"

    # symbols
    COLON = ":"
    AT = "@"
    EQUALS = "="

KEYWORDS = {
        "reg": TokenType.REG,
        "int8": TokenType.INT8
    }

class Token:
    def __init__(self, type, value, line=None):
        self.type = type
        self.value = value
        self.line = line