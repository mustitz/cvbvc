"""
This module demonstrates the usage of the CParser class to parse a C source file.

It imports the CParser class from the cparser module and uses it to parse the
specified C source file, 'demo.c', displaying the results of the parsing process.
"""

from cparser import CParser

def _main():
    fn = 'demo.c'
    cparser = CParser()
    cparser.parse(fn)

if __name__ == '__main__':
    _main()
