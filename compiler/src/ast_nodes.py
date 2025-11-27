class RegisterDecleration:
    def __init__(self, name=None, type=None, register=None, value=None):
        self.name = name
        self.type = type
        self.register = register
        self.value = value

class AddOperator:
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

class VariableAssignment:
    def __init__(self, identifier=None, value=None, value_type=None):
        self.identifier = identifier
        self.value = value
        self.value_type = value_type

class PrintFunction:
    def __init__(self, statement=None, statement_type=None):
        self.statement = statement
        self.statement_type = statement_type