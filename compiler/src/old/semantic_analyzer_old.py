from tokens import TokenType
from ast_nodes import RegisterDecleration, StackDecleration, VariableAssignment, AddOperator, MemoryAlloc

# TODO handle error handling here
class SemanticError(Exception):
    pass

class SemanticAnalyzer:
    RESERVED_KEYWORDS = [
        'int8',
        'uint8',
        'char',
        'bool',
        'reg',
        'true',
        'false',
        'add',
        'stack',
        'alloc'
    ]

    def __init__(self):
        self.symbol_table = {}
        self.used_registers = set()
        
    def analyze(self, program):
        for statement in program.statements:
            if isinstance(statement, RegisterDecleration):
                self._analyze_register_declaration(statement)
            elif isinstance(statement, StackDecleration):
                self._analyze_stack_decleration(statement, program)
            elif isinstance(statement, VariableAssignment):
                self._analyze_variable_assignment(statement)

        return self.symbol_table

    def _analyze_register_declaration(self, statement):
        if statement.name in self.RESERVED_KEYWORDS:
            raise SemanticError(f"Variable '{statement.name}' cannot be a reserved word")

        if statement.name in self.symbol_table:
            raise SemanticError(f"Variable '{statement.name}' already declared")

        if statement.register in self.used_registers:
            raise SemanticError(f"Register {statement.register} already in use")
        
        self.used_registers.add(statement.register)

        if statement.type == "int8":
            if isinstance(statement.value, AddOperator):
                number = self._analyze_add_operator(statement.name, statement.type, statement.value.left, statement.value.right)
            else:
                number = int(statement.value)
            
            if number >= -128 and number <= 127:
                self.symbol_table[statement.name] = {
                    "type": statement.type,
                    "storage": "register",
                    "register": statement.register,
                    "value": number  
                }
            else:
                raise SemanticError(f"{number} is outside of range for type int8")

        elif statement.type == "uint8":
            if isinstance(statement.value, AddOperator):
                number = self._analyze_add_operator(statement.name, statement.type, statement.value.left, statement.value.right)
            else:
                number = int(statement.value)
            
            if number >= 0 and number <= 255:
                self.symbol_table[statement.name] = {
                    "type": statement.type,
                    "storage": "register",
                    "register": statement.register,
                    "value": number  
                }
            else:
                raise SemanticError(f"{number} is outside of range for type uint8")

        elif statement.type == "char":
            character = statement.value
            if len(character) == 1:
                self.symbol_table[statement.name] = {
                    "type": statement.type,
                    "storage": "register",
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
                    "storage": "register",
                    "register": statement.register,
                    "value": statement.value
                }
            else:
                raise SemanticError(f"Only true or false values allowed for boolean type")

        else:
            raise SemanticError(f"No Type declared")

    def _analyze_stack_decleration(self, statement, program):
        if statement.name in self.RESERVED_KEYWORDS:
            raise SemanticError(f"Variable '{statement.name}' cannot be a reserved word")

        if statement.name in self.symbol_table:
            raise SemanticError(f"Variable '{statement.name}' already declared")

        memoryAllocated = False
        stackIndex = 0
        for i in range(len(program.statements)):
            if stackIndex == 0 and isinstance(program.statements[i], StackDecleration):
                stackIndex = i

            if isinstance(program.statements[i], MemoryAlloc) and stackIndex == 0:
                memoryAllocated = True
                break

            if stackIndex != 0:
                raise SemanticError(f"You must allocate memory before using stack decleration.")

        if memoryAllocated == False:
            raise SemanticError(f"You must allocate memory before using stack decleration.")

        # get current offset
        current_offset = 0
        for name, info in self.symbol_table.items():
            if info["storage"] == "stack":
                current_offset += info.get("size", 4)

        if statement.type == "int8":
            if isinstance(statement.value, AddOperator):
                number = self._analyze_add_operator(statement.name, statement.type, statement.value.left, statement.value.right)
            else:
                number = int(statement.value)
            
            if number >= -128 and number <= 127:
                self.symbol_table[statement.name] = {
                    "storage": "stack",
                    "type": statement.type,
                    "value": number,
                    "offset": current_offset,
                    "size": 4
                }
            else:
                raise SemanticError(f"{number} is outside of range for type int8")

        elif statement.type == "uint8":
            if isinstance(statement.value, AddOperator):
                number = self._analyze_add_operator(statement.name, statement.type, statement.value.left, statement.value.right)
            else:
                number = int(statement.value)
            
            if number >= 0 and number <= 255:
                self.symbol_table[statement.name] = {
                    "storage": "stack",
                    "type": statement.type,
                    "value": number,
                    "offset": current_offset,
                    "size": 4
                }
            else:
                raise SemanticError(f"{number} is outside of range for type uint8")

        elif statement.type == "char":
            character = statement.value
            if len(character) == 1:
                self.symbol_table[statement.name] = {
                    "storage": "stack",
                    "type": statement.type,
                    "value": number,
                    "offset": current_offset,
                    "size": 4  
                }
            else:
                raise SemanticError(f"Only 1 character allowed for type CHAR")

        elif statement.type == "bool":
            boolean = statement.value
            if boolean == "true" or boolean == "false":
                self.symbol_table[statement.name] = {
                    "storage": "stack",
                    "type": statement.type,
                    "value": number,
                    "offset": current_offset,
                    "size": 4  
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
                number = self._analyze_add_operator(statement.identifier, self.symbol_table[statement.identifier]["type"], statement.value.left, statement.value.right)
            
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
                number = self._analyze_add_operator(statement.identifier, self.symbol_table[statement.identifier]["type"], statement.value.left, statement.value.right)
            
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

    def _analyze_add_operator(self, identifier, type, left, right):
        number = 0

        # Process left operand
        if left in self.symbol_table:
            if self.symbol_table[left]["type"] == type:
                number = int(self.symbol_table[left]["value"])
            else:
                raise SemanticError(f"Cannot assign value of type {self.symbol_table[left]['type']} to a variable of type {type}")
        else:
            if type == "int8":
                if int(left) >= -128 and int(left) <= 127:
                    number = int(left)
                else:
                    raise SemanticError(f"{left} is outside of range for type int8")
            elif type == "uint8":
                if int(left) >= 0 and int(left) <= 255:
                    number = int(left)
                else:
                    raise SemanticError(f"{left} is outside of range for type uint8")

        # Process right operand (ADD to number)
        if right in self.symbol_table:
            if self.symbol_table[right]["type"] == type:
                number += int(self.symbol_table[right]["value"]) 
            else:
                raise SemanticError(f"Cannot assign value of type {self.symbol_table[right]['type']} to a variable of type {type}")
        else:
            if type == "int8":
                if int(right) >= -128 and int(right) <= 127:
                    number += int(right) 
                else:
                    raise SemanticError(f"{right} is outside of range for type int8")
            elif type == "uint8":
                if int(right) >= 0 and int(right) <= 255:
                    number += int(right)  
                else:
                    raise SemanticError(f"{right} is outside of range for type uint8")

        # Check final result is in range
        if type == "int8":
            if number >= -128 and number <= 127:
                return number
            else:
                raise SemanticError(f"{number} is outside of range for type int8")
        elif type == "uint8": 
            if number >= 0 and number <= 255:
                return number
            else:
                raise SemanticError(f"{number} is outside of range for type uint8")