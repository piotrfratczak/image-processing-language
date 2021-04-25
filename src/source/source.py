from .position import Position


class Source:
    def __init__(self, source_stream):
        self.source_stream = source_stream
        self.byte = None
        self.position = None
        self.char = None

    def next_char(self):
        pass


class FileSource(Source):
    def __init__(self, file):
        super(FileSource, self).__init__(file)
        self.byte = 0
        self.position = Position()

    def next_char(self):
        self.char = self.source_stream.read(1)
        self.byte += 1
        if self.char == '\n':
            self.position.next_line()
        else:
            self.position.next_column()
