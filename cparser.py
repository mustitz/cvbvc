"""
This module defines a CParser class and related components to parse C source files.

It includes definitions for LexemeType, Lexeme, and helper functions to process
lines from the source file into lexemes.
"""

from collections import namedtuple
from enum import Enum, auto
from itertools import groupby
from pathlib import Path

from utils import format_ranges

class LexemeType(Enum):
    """Enumeration for lexeme types in the parser."""
    LEX_UNKNOWN = auto()
    LEX_RLINE = auto()
    LEX_CLINE = auto()

Loc = namedtuple('Loc', ['l', 'c'])

class Lexeme:
    """Represents a lexical element with type, text, and loc information."""

    def __init__(self):
        self.type = LexemeType.LEX_UNKNOWN
        self.text = ''
        self.locs = []

    def _format_locs(self):
        def format_lines():
            for l, locs in groupby(self.locs, key=lambda pos: pos.l):
                ranges = format_ranges(pos.c for pos in locs)
                yield f"{l}:{ranges}"

        return ';'.join(format_lines())

    @property
    def last_pos(self):
        """
        Retrieves the last position from the locs list.

        Returns:
            The last Loc object for the last character in a lexeme.
        """
        return self.locs[-1]

    def append(self, lexeme):
        """
        Appends the text and location information from another Lexeme object to this one.

        Args:
            lexeme (Lexeme): The Lexeme object whose text and locs are to be appended.
        """

        self.text += lexeme.text
        self.locs += lexeme.locs

    def truncate(self, count=1):
        """
        Truncates the last 'count' characters and location entries from the lexeme's text and locs.

        Args:
            count (int): The number of characters and location entries to truncate. Defaults to 1.
        """

        if count > 0:
            self.text = self.text[:-count]
            self.locs = self.locs[:-count]

    def endswith(self, s):
        """
        Checks if the lexeme's text ends with a given substring.

        Args:
            s (str): The substring to check against the end of the lexeme's text.
        """
        return self.text.endswith(s)

    def dump(self):
        """Returns a string representation of the lexeme."""
        locs = self._format_locs()
        return f'Lexeme(type={self.type.name}, text={self.text}, locs={locs})'

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

    def _read_clines(self, rlines):
        current = None
        while True:
            try:
                rline = next(rlines)
            except StopIteration:
                break

            if current is None:
                current = rline
            else:
                current.type = LexemeType.LEX_CLINE
                current.append(rline)

            if not current.endswith('\\'):
                yield current
                current = None
            else:
                current.truncate()

        if current is not None:
            self.error(current.last_pos, "Slashed end", dc=1)
            yield current

    def error(self, pos, msg, *, dl=0, dc=0):
        """
        Prints an error message with file name, line, and column information.

        Args:
            pos (Position): The position object containing line and column information.
            msg (str): The error message to be displayed.
            dl (int, optional): The line number correction. Defaults to 0.
            dc (int, optional): The column number correction. Defaults to 0.

        Prints:
            str: A formatted error message with location.
        """

        l, c = pos.l + dl, pos.c + dc
        print(f'Error {self.fn}:{l}:{c} {msg}')

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
            stream = self._read_clines(stream)
            self.dump_stream(stream)
