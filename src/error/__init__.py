class ShuttleError(Exception):
    def __init__(self, reason):
        self.message = reason