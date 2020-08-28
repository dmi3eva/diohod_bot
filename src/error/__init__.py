class CompilationError(Exception):
    def __init__(self, reason):
        self.message = reason


class ActionError(Exception):
    def __init__(self, reason):
        self.message = reason