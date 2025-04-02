"""
This module defines a CParser class and related components to parse C source files.

It includes definitions for LexemeType, Lexeme, and helper functions to process
lines from the source file into lexemes.
"""

from collections import namedtuple
from pathlib import Path
from enum import Enum, auto

class LexemeType(Enum):
    """Enumeration for lexeme types in the parser."""
    LEX_UNKNOWN = auto()
    LEX_RLINE = auto()

Loc = namedtuple('Loc', ['l', 'c'])

class Lexeme: #pylint: disable=too-few-public-methods
    """Represents a lexical element with type, text, and loc information."""

    def __init__(self):
        self.type = LexemeType.LEX_UNKNOWN
        self.text = ''
        self.locs = []

    def dump(self):
        """Returns a string representation of the lexeme."""
        return f'Lexeme(type={self.type.name}, text={self.text}, locs={self.locs})'

def make_line(num, line):
    """
    Creates a Lexeme object from a given line of text.

    Args:
        num (int): The line number in the source file.
        line (str): The text content of the line.

    Returns:
        Lexeme: A Lexeme object representing the line.
    """
    lexem = Lexeme()
    lexem.text = line
    lexem.locs = [Loc(num, c+1) for c in range(len(line))]
    lexem.type = LexemeType.LEX_RLINE
    return lexem

class CParser:
    """Parser for C source files."""

    def __init__(self):
        self.fn = None

    def _read_rlines(self, f):
        num = 1
        for line in f.readlines():
            if line.endswith('\n'):
                line = line[:-1]
            lexem = make_line(num, line)
            num += 1
            yield lexem

    def dump_stream(self, stream):
        """
        Prints the dump of each lexeme in the given stream.

        Args:
            stream (iterable): An iterable of Lexeme objects.
        """
        for lexem in stream:
            print(lexem.dump())

    def parse(self, fn):
        """
        Parses the given C source file and dumps its lexemes.

        Args:
            fn (str or path-like object):
                The filename or path-like object representing the C source file to parse.
        """
        self.fn = Path(fn).absolute()
        with open(self.fn, 'r', encoding='utf-8') as f:
            stream = self._read_rlines(f)
            self.dump_stream(stream)
