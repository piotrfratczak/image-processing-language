class Position:
    def __init__(self, line=1, column=0):
        self.line = line
        self.column = column

    def next_column(self):
        self.column += 1

    def next_line(self):
        self.line += 1
        self.column = 1
