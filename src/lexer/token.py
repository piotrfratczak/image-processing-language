

class Token:
    def __init__(self, token_type, position, value=None):
        self.type = token_type
        self.position = position
        self.value = value
