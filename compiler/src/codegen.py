from tokens import TokenType
from ast_nodes import RegisterDecleration, VariableAssignment, AddOperator, StackDecleration, MemoryAlloc, Comparison, IfStatement

class Codegen:
    def __init__(self, symbol_table, statements):
        self.symbol_table = symbol_table
        self.statements = statements
        self.assembly_code = []

    def generate(self):
        stack_size = 0
        for statement in self.statements:
            if isinstance(statement, MemoryAlloc):
                stack_size = int(statement.value)
                break
        self._header(stack_size)

        for statement in self.statements:
            if isinstance(statement, RegisterDecleration):
                self._generate_register_decleration(statement)
            elif isinstance(statement, VariableAssignment):
                self._generate_variable_assignment(statement)
            elif isinstance(statement, StackDecleration):
                self._generate_stack_decleration(statement)
            elif isinstance(statement, IfStatement):
                self._generate_if_statement(statement)

        self._footer(stack_size)
        return '\n'.join(self.assembly_code)

    def _header(self, stack_size):
        # TODO: Add allocation for functions 
        self.assembly_code.append('.global _start')
        self.assembly_code.append('.align 2')
        self.assembly_code.append('')
        self.assembly_code.append('_start:')

        if stack_size > 0:
            self.assembly_code.append(f'    sub sp, sp, #{stack_size}')

        self.assembly_code.append('')
        
    def _footer(self, stack_size):
        if stack_size > 0:
            self.assembly_code.append(f'    add sp, sp, #{stack_size}')

        self.assembly_code.append('')
        self.assembly_code.append('    mov x0, #0')
        self.assembly_code.append('    mov x16, #1')
        self.assembly_code.append('    svc #0x80')

    def _generate_register_decleration(self, statement):
        if statement.type == 'int8' or statement.type == 'uint8':
            value = self.symbol_table[statement.name]['value']
            self.assembly_code.append(f'    mov {statement.register}, #{value}')
        elif statement.type == 'bool':
            value = self.symbol_table[statement.name]['value']
            if value == 'true' or value == True or value == 1:
                self.assembly_code.append(f'    mov {statement.register}, #1')
            else:
                self.assembly_code.append(f'    mov {statement.register}, #0')
        elif statement.type == 'char':
            value = self.symbol_table[statement.name]['value']
            self.assembly_code.append(f'    mov {statement.register}, #{ord(value)}')

        self.assembly_code.append('')

    def _generate_variable_assignment(self, statement):
        if statement.value in self.symbol_table:
            self.assembly_code.append(f'    mov {self.symbol_table[statement.identifier]['register']}, {self.symbol_table[statement.value]['register']}')
        elif isinstance(statement.value, AddOperator):
            # can only have 1 register per add and register has to be on the left
            if statement.value.left not in self.symbol_table and statement.value.right not in self.symbol_table:
                self.assembly_code.append(f'    mov {self.symbol_table[statement.identifier]['register']}, #{statement.value.left}')
                self.assembly_code.append(f'    add {self.symbol_table[statement.identifier]['register']}, {self.symbol_table[statement.identifier]['register']}, #{statement.value.right}')
            else:
                left_value = ''
                if statement.value.left in self.symbol_table:
                    left_value = self.symbol_table[statement.value.left]['register']
                else:
                    left_value = f'#{statement.value.left}'

                right_value = ''
                if statement.value.right in self.symbol_table:
                    right_value = self.symbol_table[statement.value.right]['register']
                else:
                    right_value = f'#{statement.value.right}'

                if left_value.startswith('#'):
                    self.assembly_code.append(f'    add {self.symbol_table[statement.identifier]['register']}, {right_value}, {left_value}')
                else:   
                    self.assembly_code.append(f'    add {self.symbol_table[statement.identifier]['register']}, {left_value}, {right_value}')
        else:
            if statement.value_type == TokenType.NUMBER:
                self.assembly_code.append(f'    mov {self.symbol_table[statement.identifier]['register']}, #{statement.value}')
            elif statement.value_type == TokenType.CHARACTER:
                self.assembly_code.append(f'    mov {self.symbol_table[statement.identifier]['register']}, #{ord(statement.value)}')
            elif statement.value_type == TokenType.TRUE:
                self.assembly_code.append(f'    mov {self.symbol_table[statement.identifier]['register']}, #1')
            elif statement.value_type == TokenType.FALSE:
                self.assembly_code.append(f'    mov {self.symbol_table[statement.identifier]['register']}, #0')
        
        self.assembly_code.append('')

    def _generate_stack_decleration(self, statement):
        offset = self.symbol_table[statement.name]["offset"]
        value = self.symbol_table[statement.name]["value"]

        self.assembly_code.append(f'    mov x8, #{value}')
        self.assembly_code.append(f'    str x8, [sp, #{offset}]')

        self.assembly_code.append('')

    def _generate_if_statement(self, statement):
        print()
