class LexerError(Exception):
    def __init__(self, message, line):
        self.message = message
        self.line = line
        error_msg = f"LEXER ERROR @ Line {line}: {message}"
        super().__init__(error_msg)  # Pass to Exception