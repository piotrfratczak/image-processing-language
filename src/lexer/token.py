class Token:
    def __init__(self, token_type, text_position, byte_position, value=None):
        self.type = token_type
        self.text_position = text_position
        self.byte_position = byte_position
        self.value = value
