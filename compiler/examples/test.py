import sys
import os
import subprocess
sys.path.append('../src') 

from lexer import Lexer

with open('test.gala', 'r') as f:
    source_code = f.read()

print("\n##### LEXER #####")
lexer = Lexer(source_code)
tokens = lexer.tokenize()

for token in tokens:
    print(f"Token(type={token.type}, value='{token.value}', line={token.line})")