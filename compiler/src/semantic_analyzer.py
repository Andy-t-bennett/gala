from tokens import TokenType
from ast_nodes import RegisterDecleration, VariableAssignment, AddOperator, PrintFunction

# TODO handle error handling here
class SemanticError(Exception):
    pass

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}
        self.used_registers = set()

    def analyze(self, program):
        for statement in program.statements:
            if isinstance(statement, RegisterDecleration):
                self._analyze_register_declaration(statement)
            elif isinstance(statement, VariableAssignment):
                self._analyze_variable_assignment(statement)
            elif isinstance(statement, PrintFunction):
                self._analyze_print_function(statement)

        return self.symbol_table

    def _analyze_register_declaration(self, statement):
        reserved_words = [
            'int8',
            'uint8',
            'char',
            'bool',
            'reg',
            'print',
            'true',
            'false',
            'add',
            'sub'
        ]

        if statement.name in reserved_words:
            raise SemanticError(f"Variable '{statement.name}' cannot be a reserved word")

        if statement.name in self.symbol_table:
            raise SemanticError(f"Variable '{statement.name}' already declared")

        if statement.register in self.used_registers:
            raise SemanticError(f"Register {statement.register} already in use")
        
        self.used_registers.add(statement.register)

        if statement.type == "int8":
            number = int(statement.value)
            if number >= -128 and number <= 127:
                self.symbol_table[statement.name] = {
                    "type": statement.type,
                    "register": statement.register,
                    "value": statement.value
                }
            else:
                raise SemanticError(f"{statement.value} is outside of range for type int8")

        elif statement.type == "uint8":
            number = int(statement.value)
            if number >= 0 and number <= 255:
                self.symbol_table[statement.name] = {
                    "type": statement.type,
                    "register": statement.register,
                    "value": statement.value
                }
            else:
                raise SemanticError(f"{statement.value} is outside of range for type uint8")

        elif statement.type == "char":
            character = statement.value
            if len(character) == 1:
                self.symbol_table[statement.name] = {
                    "type": statement.type,
                    "register": statement.register,
                    "value": statement.value
                }
            else:
                raise SemanticError(f"Only 1 character allowed for type CHAR")

        elif statement.type == "bool":
            boolean = statement.value
            if boolean == "true" or boolean == "false":
                self.symbol_table[statement.name] = {
                    "type": statement.type,
                    "register": statement.register,
                    "value": statement.value
                }
            else:
                raise SemanticError(f"Only true or false values allowed for boolean type")

        else:
            raise SemanticError(f"No Type declared")

    def _analyze_variable_assignment(self, statement):
        if statement.identifier not in self.symbol_table:
            raise SemanticError(f"Variable '{statement.identifier}' hasn't been declared yet")

        if self.symbol_table[statement.identifier]["type"] == "int8":
            number = 0

            if statement.value in self.symbol_table:
                type = self.symbol_table[statement.value]["type"]
                if type != self.symbol_table[statement.identifier]["type"]:
                    raise SemanticError(f"Cannot assign value of type {type} to a variable of type {self.symbol_table[statement.identifier]["type"]}")
                number = int(self.symbol_table[statement.value]["value"])
            
            elif isinstance(statement.value, AddOperator):
                if statement.value.left in self.symbol_table:
                    if self.symbol_table[statement.value.left]["type"] == self.symbol_table[statement.identifier]["type"]:
                        number = int(self.symbol_table[statement.value.left]["value"])
                    else:
                        raise SemanticError(f"Cannot assign value of type {self.symbol_table[statement.value.left]["type"]} to a variable of type {self.symbol_table[statement.identifier]["type"]}")
                else:
                    if int(statement.value.left) >= -128 and int(statement.value.left) <= 127:
                        number = int(statement.value.left)
                    else:
                        raise SemanticError(f"{statement.value.left} is outside of range for type int8")

                if statement.value.right in self.symbol_table:
                    if self.symbol_table[statement.value.right]["type"] == self.symbol_table[statement.identifier]["type"]:
                        number += int(self.symbol_table[statement.value.right]["value"])
                    else:
                        raise SemanticError(f"Cannot assign value of type {self.symbol_table[statement.value.right]["type"]} to a variable of type {self.symbol_table[statement.identifier]["type"]}")
                else:
                    if int(statement.value.right) >= -128 and int(statement.value.right) <= 127:
                        number += int(statement.value.right)
                    else:
                        raise SemanticError(f"{statement.value.right} is outside of range for type int8")

            else:
                number = int(statement.value)

            if number >= -128 and number <= 127:
                self.symbol_table[statement.identifier]["value"] = number
            else:
                raise SemanticError(f"{statement.value} is outside of range for type int8")

        elif self.symbol_table[statement.identifier]["type"] == "uint8":
            number = 0

            if statement.value in self.symbol_table:
                type = self.symbol_table[statement.value]["type"]
                if type != self.symbol_table[statement.identifier]["type"]:
                    raise SemanticError(f"Cannot assign value of type {type} to a variable of type {self.symbol_table[statement.identifier]["type"]}")
                number = int(self.symbol_table[statement.value]["value"])
            elif isinstance(statement.value, AddOperator):
                if statement.value.left in self.symbol_table:
                    if self.symbol_table[statement.value.left]["type"] == self.symbol_table[statement.identifier]["type"]:
                        number = int(self.symbol_table[statement.value.left]["value"])
                    else:
                        raise SemanticError(f"Cannot assign value of type {self.symbol_table[statement.value.left]["type"]} to a variable of type {self.symbol_table[statement.identifier]["type"]}")
                else:
                    if int(statement.value.left) >= 0 and int(statement.value.left) <= 255:
                        number = int(statement.value.left)
                    else:
                        raise SemanticError(f"{statement.value.left} is outside of range for type uint8")

                if statement.value.right in self.symbol_table:
                    if self.symbol_table[statement.value.right]["type"] == self.symbol_table[statement.identifier]["type"]:
                        number += int(self.symbol_table[statement.value.right]["value"])
                    else:
                        raise SemanticError(f"Cannot assign value of type {self.symbol_table[statement.value.right]["type"]} to a variable of type {self.symbol_table[statement.identifier]["type"]}")
                else:
                    if int(statement.value.right) >= 0 and int(statement.value.right) <= 255:
                        number += int(statement.value.right)
                    else:
                        raise SemanticError(f"{statement.value.right} is outside of range for type uint8") 
            else:
                number = int(statement.value)

            if number >= 0 and number <= 255:
                self.symbol_table[statement.identifier]["value"] = number
            else:
                raise SemanticError(f"{statement.value} is outside of range for type uint8")

        elif self.symbol_table[statement.identifier]["type"] == "char":
            character = ''

            if statement.value_type == TokenType.IDENTIFIER and statement.value in self.symbol_table:
                type = self.symbol_table[statement.value]["type"]
                if type != self.symbol_table[statement.identifier]["type"]:
                    raise SemanticError(f"Cannot assign value of type {type} to a variable of type {self.symbol_table[statement.identifier]["type"]}")
                character = self.symbol_table[statement.value]["value"]
            else:
                character = statement.value

            if len(character) == 1:
                self.symbol_table[statement.identifier]["value"] = character
            else:
                raise SemanticError(f"{statement.value} can only be 1 character")

        elif self.symbol_table[statement.identifier]["type"] == "bool":
            boolean = ''

            if statement.value in self.symbol_table:
                type = self.symbol_table[statement.value]["type"]
                if type != self.symbol_table[statement.identifier]["type"]:
                    raise SemanticError(f"Cannot assign value of type {type} to a variable of type {self.symbol_table[statement.identifier]["type"]}")
                boolean = self.symbol_table[statement.value]["value"]
            else:
                boolean = statement.value    

            if boolean == 'true' or boolean == 'false':
                self.symbol_table[statement.identifier]["value"] = boolean
            else:
                raise SemanticError(f"{statement.identifier} can only be true or false")        

    def _analyze_print_function(self, statement):
        if statement.statement_type == TokenType.IDENTIFIER and statement.statement not in self.symbol_table:
            raise SemanticError(f"Variable '{statement.statement}' hasn't been declared yet")


    