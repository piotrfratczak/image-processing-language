from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.interpreter.interpreter import Interpreter
from src.source.source import FileSource
import sys


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('\nUsage:')
        print('python3 imli.py <source_file>\n')
        exit(0)

    source_file_path = sys.argv[1]
    source_file = open(source_file_path)

    lexer = Lexer(FileSource(source_file))
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    returned = interpreter.interpret()

    print('\n\nFinished with return code: {}.'.format(returned))

    source_file.close()
