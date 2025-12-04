from ast_nodes import RegisterDecleration, StackDecleration, VariableAssignment, AddOperator, MemoryAlloc
from tokens import TokenType

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def parse(self):
        program = Program()

        while self.position < len(self.tokens):
            token = self.tokens[self.position]

            if token.type == TokenType.REG:
                program.statements.append(self._parse_register_decleration())
            elif token.type == TokenType.STACK:
                program.statements.append(self._parse_stack_decleration())
            elif token.type == TokenType.IDENTIFIER:
                program.statements.append(self._parse_variable_assignment())
            elif token.type == TokenType.ALLOC:
                program.statements.append(self._parse_memory_allocation())
            else:
                self.position += 1

        return program

    def _parse_register_decleration(self):
        registerDecleration = RegisterDecleration()
        registerDecleration.register = self.tokens[self.position].value
        registerDecleration.storage = "register"
        self.position += 1

        if self.tokens[self.position].type == TokenType.IDENTIFIER:
            registerDecleration.name = self.tokens[self.position].value
            self.position += 1
        else:
            raise SyntaxError("REGISTER DECLERATION: Expected identifier")

        if self.tokens[self.position].type == TokenType.COLON:
            self.position += 1
        else:
            raise SyntaxError("REGISTER DECLERATION: Expected colon")

        # Types
        if self.tokens[self.position].type == TokenType.INT8 or self.tokens[self.position].type == TokenType.UINT8 or self.tokens[self.position].type == TokenType.BOOL or self.tokens[self.position].type == TokenType.CHAR:
            registerDecleration.type = self.tokens[self.position].value
            self.position += 1
        else:
            raise SyntaxError("REGISTER DECLERATION: Expected Type")

        if self.tokens[self.position].type == TokenType.AT:
            self.position += 1
        else:
            raise SyntaxError("REGISTER DECLERATION: Expected @")

        if self.tokens[self.position].type == TokenType.REGISTER:
            registerDecleration.register = self.tokens[self.position].value
            self.position += 1
        else:
            raise SyntaxError("REGISTER DECLERATION: Expected General Purpose Register Value ('x9', 'x10', 'x11', 'x12', 'x13', 'x14', 'x15')")

        if self.tokens[self.position].type == TokenType.EQUALS:
            self.position += 1
        else:
            raise SyntaxError("REGISTER DECLERATION: Expected =")

        # value
        if self.tokens[self.position].type == TokenType.NUMBER or self.tokens[self.position].type == TokenType.CHARACTER or self.tokens[self.position].type == TokenType.TRUE or self.tokens[self.position].type == TokenType.FALSE:
            registerDecleration.value = self.tokens[self.position].value
            self.position += 1
        elif self.tokens[self.position].type == TokenType.ADD:
            registerDecleration.value = self._parse_add_operator()
        else:
            raise SyntaxError("REGISTER DECLERATION: Expecting Value")

        return registerDecleration

    def _parse_stack_decleration(self):
        stackDecleration = StackDecleration()
        stackDecleration.register = self.tokens[self.position].value
        stackDecleration.storage = "stack"
        self.position += 1

        if self.tokens[self.position].type == TokenType.IDENTIFIER:
            stackDecleration.name = self.tokens[self.position].value
            self.position += 1
        else:
            raise SyntaxError("STACK DECLERATION: Expected identifier")

        if self.tokens[self.position].type == TokenType.COLON:
            self.position += 1
        else:
            raise SyntaxError("STACK DECLERATION: Expected colon")

        # Types
        if self.tokens[self.position].type == TokenType.INT8 or self.tokens[self.position].type == TokenType.UINT8 or self.tokens[self.position].type == TokenType.BOOL or self.tokens[self.position].type == TokenType.CHAR:
            stackDecleration.type = self.tokens[self.position].value
            self.position += 1
        else:
            raise SyntaxError("STACK DECLERATION: Expected Type")

        if self.tokens[self.position].type == TokenType.EQUALS:
            self.position += 1
        else:
            raise SyntaxError("STACK DECLERATION: Expected =")

        # value
        if self.tokens[self.position].type == TokenType.NUMBER or self.tokens[self.position].type == TokenType.CHARACTER or self.tokens[self.position].type == TokenType.TRUE or self.tokens[self.position].type == TokenType.FALSE:
            stackDecleration.value = self.tokens[self.position].value
            self.position += 1
        elif self.tokens[self.position].type == TokenType.ADD:
            stackDecleration.value = self._parse_add_operator()
        else:
            raise SyntaxError("STACK DECLERATION: Expecting Value")

        return stackDecleration

    def _parse_variable_assignment(self):
        variableAssignment = VariableAssignment()
        variableAssignment.identifier = self.tokens[self.position].value
        
        # chack for missing register
        if self.tokens[self.position + 1].type == TokenType.COLON:
            raise SyntaxError("VARIABLE ASSIGNMENT: Missing reg Keyword")
        else:
            self.position += 1

        if self.tokens[self.position].type == TokenType.EQUALS:
            self.position += 1
        else:
            raise SyntaxError("VARIABLE ASSIGNMENT: Expected =")
        
        if self.tokens[self.position].type == TokenType.IDENTIFIER or self.tokens[self.position].type == TokenType.NUMBER or self.tokens[self.position].type == TokenType.CHARACTER or self.tokens[self.position].type == TokenType.TRUE or self.tokens[self.position].type == TokenType.FALSE or self.tokens[self.position].type == TokenType.ADD:
            if self.tokens[self.position].type == TokenType.IDENTIFIER or self.tokens[self.position].type == TokenType.NUMBER or self.tokens[self.position].type == TokenType.CHARACTER or self.tokens[self.position].type == TokenType.TRUE or self.tokens[self.position].type == TokenType.FALSE:
                variableAssignment.value = self.tokens[self.position].value
                variableAssignment.value_type = self.tokens[self.position].type
                self.position += 1
            elif self.tokens[self.position].type == TokenType.ADD:
                variableAssignment.value = self._parse_add_operator()
        else:
            raise SyntaxError("VARIABLE ASSIGNMENT: Expected Value")

        return variableAssignment

    def _parse_add_operator(self):
        addOperator = AddOperator()
        self.position += 1

        if self.tokens[self.position].type == TokenType.L_PAREN:
            self.position += 1
        else:
            raise SyntaxError("ADD OPERATOR: Expected (")

        if self.tokens[self.position].type == TokenType.IDENTIFIER or self.tokens[self.position].type == TokenType.NUMBER:
            addOperator.left = self.tokens[self.position].value
            self.position += 1
        else:
            raise SyntaxError("ADD OPERATOR: Expected a number")

        if self.tokens[self.position].type == TokenType.COMA:
            self.position += 1
        else:
            raise SyntaxError("ADD OPERATOR: Expected ,")

        if self.tokens[self.position].type == TokenType.IDENTIFIER or self.tokens[self.position].type == TokenType.NUMBER:
            addOperator.right = self.tokens[self.position].value
            self.position += 1
        else:
            raise SyntaxError("ADD OPERATOR: Expected a number")

        if self.tokens[self.position].type == TokenType.R_PAREN:
            self.position += 1
        else:
            raise SyntaxError("ADD OPERATOR: Expected )")

        return addOperator

    def _parse_memory_allocation(self):
        memoryAlloc = MemoryAlloc()
        self.position += 1

        if self.tokens[self.position].type == TokenType.L_PAREN:
            self.position += 1
        else:
            raise SyntaxError("ALLOC: Expected (")

        if self.tokens[self.position].type == TokenType.STACK:
            memoryAlloc.storage = "stack"
            self.position += 1
        else:
            raise SyntaxError("ALLOC: Expected a storage type")

        if self.tokens[self.position].type == TokenType.COMA:
            self.position += 1
        else:
            raise SyntaxError("ALLOC: Expected ,")

        if self.tokens[self.position].type == TokenType.NUMBER:
            memoryAlloc.value = self.tokens[self.position].value
            self.position += 1
        else:
            raise SyntaxError("ALLOC: Expected a byte allocation")

        if self.tokens[self.position].type == TokenType.R_PAREN:
            self.position += 1
        else:
            raise SyntaxError("ALLOC: Expected )")

        return memoryAlloc


class Program:
    def __init__(self, statements=None):
        self.statements = statements or []
