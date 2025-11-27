from ast_nodes import RegisterDecleration, VariableAssignment, AddOperator, PrintFunction
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
            elif token.type == TokenType.PRINT:
                program.statements.append(self._parse_print_function())
            elif token.type == TokenType.IDENTIFIER:
                program.statements.append(self._parse_variable_assignment())
            else:
                self.position += 1

        return program

    def _parse_register_decleration(self):
        registerDecleration = RegisterDecleration()
        registerDecleration.register = self.tokens[self.position].value
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

    def _parse_print_function(self):
        printFunction = PrintFunction()
        self.position += 1

        if self.tokens[self.position].type == TokenType.L_PAREN:
            self.position += 1
        else:
            raise SyntaxError("PRINT FUNCTION: Expected (")

        if self.tokens[self.position].type == TokenType.NUMBER or self.tokens[self.position].type == TokenType.CHARACTER or self.tokens[self.position].type == TokenType.TRUE or self.tokens[self.position].type == TokenType.FALSE or self.tokens[self.position].type == TokenType.IDENTIFIER:
            printFunction.statement = self.tokens[self.position].value
            printFunction.statement_type = self.tokens[self.position].type
            self.position += 1
        else:
            raise SyntaxError("PRINT FUNCTION: Expected statement")

        if self.tokens[self.position].type == TokenType.R_PAREN:
            self.position += 1
        else:
            raise SyntaxError("PRINT FUNCTION: Expected )")

        return printFunction

class Program:
    def __init__(self, statements=None):
        self.statements = statements or []
