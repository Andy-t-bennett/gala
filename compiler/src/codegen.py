from tokens import TokenType
from ast_nodes import RegisterDecleration, VariableAssignment, AddOperator, PrintFunction

class Codegen:
    def __init__(self, symbol_table, statements):
        self.symbol_table = symbol_table
        self.statements = statements
        self.assembly_code = []

    def generate(self):
        self._header()

        for statement in self.statements:
            if isinstance(statement, RegisterDecleration):
                self._generate_register_decleration(statement)
            elif isinstance(statement, VariableAssignment):
                self._generate_variable_assignment(statement)
            elif isinstance(statement, PrintFunction):
                self._generate_print(statement)

        self._footer()
        return '\n'.join(self.assembly_code)

    def _header(self):
        self.assembly_code.append('.global _main')
        self.assembly_code.append('.align 2')
        self.assembly_code.append('')
        self.assembly_code.append('_main:')
        # allocate space for c library (printf)
        self.assembly_code.append('    sub sp, sp, #32')
        self.assembly_code.append('    stp x29, x30, [sp, #16]')
        self.assembly_code.append('    add x29, sp, #16')
        
    def _footer(self):
        self.assembly_code.append('')
        self.assembly_code.append('    ldp x29, x30, [sp, #16]')
        self.assembly_code.append('    add sp, sp, #32')
        self.assembly_code.append('    mov w0, #0')
        self.assembly_code.append('    ret')
        self.assembly_code.append('')
        self.assembly_code.append('.data')
        self.assembly_code.append('fmt_num: .asciz "%d\\n"')
        self.assembly_code.append('fmt_char: .asciz "%c\\n"')

    def _generate_register_decleration(self, statement):
        if statement.type == 'int8' or statement.type == 'uint8':
            self.assembly_code.append(f'    mov {statement.register}, #{statement.value}')
        elif statement.type == 'bool':
            if statement.value == 'true':
                self.assembly_code.append(f'    mov {statement.register}, #1')
            else:
                self.assembly_code.append(f'    mov {statement.register}, #0')
        elif statement.type == 'char':
            self.assembly_code.append(f'    mov {statement.register}, #{ord(statement.value)}')

    def _generate_variable_assignment(self, statement):
        if statement.value in self.symbol_table:
            self.assembly_code.append(f'    mov {self.symbol_table[statement.identifier]['register']}, {self.symbol_table[statement.value]['register']}')
        elif isinstance(statement.value, AddOperator):
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

    def _generate_print(self, statement):
        if statement.statement in self.symbol_table:
            var_type = self.symbol_table[statement.statement]['type']
            var_register = self.symbol_table[statement.statement]['register']
            w_register = var_register.replace('x', 'w')
            
            if var_type in ['int8', 'uint8', 'bool']:
                self.assembly_code.append(f'    uxtb x8, {w_register}')
                self.assembly_code.append('    str x8, [sp]')
                self.assembly_code.append('    adrp x0, fmt_num@PAGE')
                self.assembly_code.append('    add x0, x0, fmt_num@PAGEOFF')
                self.assembly_code.append('    bl _printf')
            
            elif var_type == 'char':
                self.assembly_code.append(f'    uxtb x8, {w_register}')
                self.assembly_code.append('    str x8, [sp]')
                self.assembly_code.append('    adrp x0, fmt_char@PAGE')
                self.assembly_code.append('    add x0, x0, fmt_char@PAGEOFF')
                self.assembly_code.append('    bl _printf')

        else:
            if statement.statement_type == TokenType.NUMBER:
                self.assembly_code.append(f'    mov x8, #{statement.statement}')
                self.assembly_code.append('    str x8, [sp]')
                self.assembly_code.append('    adrp x0, fmt_num@PAGE')
                self.assembly_code.append('    add x0, x0, fmt_num@PAGEOFF')
                self.assembly_code.append('    bl _printf')
            elif statement.statement_type == TokenType.TRUE:
                self.assembly_code.append('    mov x8, #1')
                self.assembly_code.append('    str x8, [sp]')
                self.assembly_code.append('    adrp x0, fmt_num@PAGE')
                self.assembly_code.append('    add x0, x0, fmt_num@PAGEOFF')
                self.assembly_code.append('    bl _printf')
            elif statement.statement_type == TokenType.FALSE:
                self.assembly_code.append('    mov x8, #0')
                self.assembly_code.append('    str x8, [sp]')
                self.assembly_code.append('    adrp x0, fmt_num@PAGE')
                self.assembly_code.append('    add x0, x0, fmt_num@PAGEOFF')
                self.assembly_code.append('    bl _printf')
            elif statement.statement_type == TokenType.CHARACTER:
                self.assembly_code.append(f'    mov x8, #{ord(statement.statement)}')
                self.assembly_code.append('    str x8, [sp]')
                self.assembly_code.append('    adrp x0, fmt_char@PAGE')
                self.assembly_code.append('    add x0, x0, fmt_char@PAGEOFF')
                self.assembly_code.append('    bl _printf')