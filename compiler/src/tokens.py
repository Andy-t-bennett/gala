from enum import Enum, auto

class TokenType(Enum):
    # types
    INT8 = auto()
    UINT8 = auto()
    BOOL = auto()
    CHAR = auto()

    # keywords
    REG = auto()
    PRINT = auto()
    CLEAR = auto()

    # identifiers and values
    IDENTIFIER = auto()
    REGISTER = auto()
    NUMBER = auto()
    CHARACTER = auto()
    TRUE = auto()
    FALSE = auto()

    # symbols
    COLON = auto()
    AT = auto()
    L_PAREN = auto()
    R_PAREN = auto()
    COMA = auto()
    
    # operators
    EQUALS = auto()
    ADD = auto()
    SUB = auto()

    EOF = auto()


class Token:
    def __init__(self, type: TokenType, value: str):
        self.type = type
        self.value = value