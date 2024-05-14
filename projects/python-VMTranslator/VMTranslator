#!/usr/bin/env python3

import sys
import os

from parser import Parser
from code_writer import CodeWriter

if len(sys.argv) != 2:
    print("Usage: ./VMTtranslator filename.vm")
    sys.exit(1)

file_name = os.path.basename(sys.argv[1]).split('.')[0]
output_file_path = sys.argv[1].rsplit('.', 1)[0] + ".asm"
parserInstance = Parser(sys.argv[1])
writerInstance = CodeWriter(file_name, output_file_path)

while parserInstance.advance():
    print(parserInstance.command_type, parserInstance.arg1, parserInstance.arg2)
    writerInstance.write_code_line(parserInstance.command_type, parserInstance.arg1, parserInstance.arg2)
