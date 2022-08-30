class CompilationError(Exception):
    def __init__(self, reason):
        self.message = reason


class ActionError(Exception):
    def __init__(self, reason):
        self.message = reason


class PlanetError(Exception):
    def __init__(self, message):
        super(PlanetError, self).__init__()
        self.message = message