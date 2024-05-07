#!/usr/bin/env python3

import sys

from parser import Parser
from code_writer import CodeWriter

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python your_program.py filename.vm")
        sys.exit(1)

    file_name = sys.argv[1].rsplit('.', 1)[0]
    parserInstance = Parser(file_name)
    writerInstance = CodeWriter(file_name)

    while parserInstance.advance():
        print(parserInstance.command_type, parserInstance.arg1, parserInstance.arg2)
        writerInstance.write_code_line(parserInstance.command_type, parserInstance.arg1, parserInstance.arg2)
