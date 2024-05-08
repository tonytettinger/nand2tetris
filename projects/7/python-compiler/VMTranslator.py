#!/usr/bin/env python3
import re
import sys


from parser import Parser
from code_writer import CodeWriter

if __name__ == "__main__":
    input_file = sys.argv[1]

    file_name_no_ext = input_file.rsplit(".", 1)[0]

    file_name = re.split(r'[\\/]', file_name_no_ext)[-1]
    input_vm_file = file_name_no_ext + ".vm"
    output_asm_file = file_name_no_ext + '.asm'

    parserInstance = Parser(input_vm_file)
    writerInstance = CodeWriter(file_name, output_asm_file)

    while parserInstance.advance():
        print(parserInstance.command_type, parserInstance.arg1, parserInstance.arg2)
        writerInstance.write_code_line(parserInstance.command_type, parserInstance.arg1, parserInstance.arg2)
