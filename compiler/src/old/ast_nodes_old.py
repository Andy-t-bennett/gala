class RegisterDecleration:
    def __init__(self, name=None, storage=None, type=None, register=None, value=None):
        self.name = name
        self.storage = storage
        self.type = type
        self.register = register
        self.value = value

class StackDecleration:
    def __init__(self, name=None, storage=None, type=None, value=None, offset=None, size=None):
        self.name = name
        self.storage = storage
        self.type = type
        self.value = value
        self.offset = offset
        self.size = size

class AddOperator:
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

class VariableAssignment:
    def __init__(self, identifier=None, value=None, value_type=None):
        self.identifier = identifier
        self.value = value
        self.value_type = value_type

class MemoryAlloc:
    def __init__(self, storage=None, value=None):
        self.storage = storage
        self.value = value