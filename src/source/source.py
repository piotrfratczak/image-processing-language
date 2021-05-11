from os import linesep
from .position import Position


class Source:
    def __init__(self, source_stream):
        self.source_stream = source_stream
        self.byte = None
        self.position = None
        self.char = None
        self.is_eof = False

    def next_char(self):
        pass


class FileSource(Source):
    def __init__(self, file):
        super(FileSource, self).__init__(file)
        self.position = Position()
        self.byte = 0

    def next_char(self):
        self.char = self.source_stream.read(1)
        self.byte = self.source_stream.tell()

        if self.char == '':
            self.is_eof = True
        elif self.char == linesep:
            self.position.next_line()
        else:
            self.position.next_column()
