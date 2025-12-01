import sys
import os
import subprocess
sys.path.append('../src') 

from lexer import Lexer
from parser import Parser
from ast_nodes import RegisterDecleration, StackDecleration, VariableAssignment, AddOperator, MemoryAlloc
from semantic_analyzer import SemanticAnalyzer
from codegen import Codegen

# Read source code from .gala file
with open('test.gala', 'r') as f:
    source_code = f.read()

print("\n##### LEXER #####")
lexer = Lexer(source_code)
tokens = lexer.tokenize()

for token in tokens:
    print(f"Type: {token.type.name}, Value: '{token.value}'\n")

print("\n##### PARSER #####")
parser = Parser(tokens) 
program = parser.parse()

for statement in program.statements:
    if isinstance(statement, RegisterDecleration):
        print(f"RegisterDeclaration:")
        print(f"  name: {statement.name}")
        print(f"  storage: {statement.storage}")
        print(f"  type: {statement.type}")
        print(f"  register: {statement.register}")
        print(f"  value: {statement.value}")
        
        # If value is an AddOperator, show its details
        if isinstance(statement.value, AddOperator):
            print(f"    AddOperator:")
            print(f"      left: {statement.value.left}")
            print(f"      right: {statement.value.right}")
        print()
    
    elif isinstance(statement, StackDecleration):
        print(f"StackDecleration:")
        print(f"  name: {statement.name}")
        print(f"  storage: {statement.storage}")
        print(f"  type: {statement.type}")
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

    elif isinstance(statement, MemoryAlloc):
        print(f"MemoryAlloc:")
        print(f"  storage: {statement.storage}")
        print(f"  value: {statement.value}")
        print()

print("\n##### SEMANTIC ANALYZER #####")
analyzer = SemanticAnalyzer()
semantic_table = analyzer.analyze(program)

print(semantic_table)

print("\n##### CODEGEN #####")
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

# Automatically assemble
print("\n##### ASSEMBLING #####")
asm_cmd = ['as', '-o', f'{build_dir}/output.o', output_file]
result = subprocess.run(asm_cmd, capture_output=True, text=True)
if result.returncode != 0:
    print(f"❌ Assembly failed:\n{result.stderr}")
    sys.exit(1)
print("✅ Assembly successful")

# Automatically link
print("\n##### LINKING #####")
sdk_path = subprocess.run(['xcrun', '-sdk', 'macosx', '--show-sdk-path'], 
                         capture_output=True, text=True).stdout.strip()
link_cmd = ['ld', '-o', f'{build_dir}/program', f'{build_dir}/output.o', 
            '-lSystem', '-syslibroot', sdk_path, '-e', '_start', '-arch', 'arm64']
result = subprocess.run(link_cmd, capture_output=True, text=True)
if result.returncode != 0:
    print(f"❌ Linking failed:\n{result.stderr}")
    sys.exit(1)
print("✅ Linking successful")

# Automatically run the program
print("\n##### RUNNING PROGRAM #####")
result = subprocess.run([f'{build_dir}/program'], capture_output=True, text=True)
print(f"Exit code: {result.returncode}")
if result.stdout:
    print(f"Output: {result.stdout}")
if result.stderr:
    print(f"Errors: {result.stderr}")