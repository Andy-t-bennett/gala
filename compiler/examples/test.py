import sys
import os
sys.path.append('../src') 

from lexer import Lexer
from parser import Parser
from ast_nodes import RegisterDecleration, VariableAssignment, AddOperator, PrintFunction
from semantic_analyzer import SemanticAnalyzer
from codegen import Codegen

# Read source code from .gala file
with open('test.gala', 'r') as f:
    source_code = f.read()

print("##### LEXER #####")
lexer = Lexer(source_code)
tokens = lexer.tokenize()

for token in tokens:
    print(f"Type: {token.type.name}, Value: '{token.value}'\n")

print("##### PARSER #####")
parser = Parser(tokens) 
program = parser.parse()

for statement in program.statements:
    if isinstance(statement, RegisterDecleration):
        print(f"RegisterDeclaration:")
        print(f"  name: {statement.name}")
        print(f"  type: {statement.type}")
        print(f"  register: {statement.register}")
        print(f"  value: {statement.value}")
        
        # If value is an AddOperator, show its details
        if isinstance(statement.value, AddOperator):
            print(f"    AddOperator:")
            print(f"      left: {statement.value.left}")
            print(f"      right: {statement.value.right}")
        print()
    
    elif isinstance(statement, VariableAssignment):
        print(f"VariableAssignment:")
        print(f"  identifier: {statement.identifier}")
        print(f"  value: {statement.value}")
        print(f"  value type: {statement.value_type}")

        if isinstance(statement.value, AddOperator):
            print(f"    AddOperator:")
            print(f"      left: {statement.value.left}")
            print(f"      right: {statement.value.right}")
        print()

    elif isinstance(statement, PrintFunction):
        print(f"PrintFunction:")
        print(f"  statement: {statement.statement}")
        print(f"  statement: {statement.statement_type}")
        print()

    elif isinstance(statement, ClearFunction):
        print(f"ClearFunction:")
        print(f"  identifier: {statement.identifier}")
        print()

print("##### SEMANTIC ANALYZER #####")
analyzer = SemanticAnalyzer()
semantic_table = analyzer.analyze(program)

print(semantic_table)

print("##### CODEGEN #####")
codegen = Codegen(semantic_table, program.statements)
assembly = codegen.generate()
print(assembly)


build_dir = '../build'
os.makedirs(build_dir, exist_ok=True)

# Write assembly to .s file
output_file = os.path.join(build_dir, 'output.s')
with open(output_file, 'w') as f:
    f.write(assembly)

print(f"\n✅ Assembly written to: {output_file}")
print("\nTo compile and run:")
print(f"  as -o {build_dir}/output.o {output_file}")
print(f"  ld -o {build_dir}/program {build_dir}/output.o -lSystem -syslibroot `xcrun -sdk macosx --show-sdk-path` -e _main -arch arm64")
print(f"  {build_dir}/program")