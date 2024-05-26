#!/usr/bin/env python3

import sys
import os

from parser import Parser
from code_writer import CodeWriter

def process_each_line(parserInstance, writerInstance):
    while parserInstance.advance():
        print(parserInstance.command_type, parserInstance.arg1, parserInstance.arg2)
        writerInstance.write_code_line(parserInstance.command_type, parserInstance.arg1, parserInstance.arg2)

def reset_file(file_name):
    with open(file_name, "w"):
        pass

directory = None

if len(sys.argv) == 2:
    file = os.path.basename(sys.argv[1])
    file_split = file.split('.')
    file_name = file_split[0]
    print('filename: ', file_name)
    if len(file_split) == 2:
        file_extension = file.split('.')[1]
        print('extension is', file_extension)
        output_file_path = sys.argv[1].rsplit('.', 1)[0] + ".asm"
        reset_file(output_file_path)
        parserInstance = Parser(sys.argv[1])
        writerInstance = CodeWriter(file_name, output_file_path)
        process_each_line(parserInstance, writerInstance)

    else:
        print('workingdir is', sys.argv[1])
        directory = sys.argv[1]

else:
    directory = os.getcwd()

    if directory is not None:
        try:
            print('directory is', directory)
            os.chdir(directory)
            print(f"Changed directory to {os.getcwd()}")
        except FileNotFoundError:
            print(f"Error: Directory '{directory}' does not exist.")
        except NotADirectoryError:
            print(f"Error: '{directory}' is not a directory.")
        except PermissionError:
            print(f"Error: Permission denied to change to '{directory}'.")
        files = os.listdir()
        file_name_to_write = os.path.basename(directory)
        print('FILENAME', file_name_to_write)
        output_file = file_name_to_write + ".asm"
        reset_file(output_file)

        # First, process the Sys.vm file if it exists
        if 'Sys.vm' in files:
            print('writing file ending with vm: Sys.vm')
            parserInstance = Parser('Sys.vm')

        # Then, process all other .vm files except Sys.vm
        for file_name in files:
            if file_name.endswith('.vm') and file_name != 'Sys.vm':
                print('writing file ending with vm: ', file_name)
                parserInstance = Parser(file_name)
                writerInstance = CodeWriter(file_name_to_write, output_file)
                process_each_line(parserInstance, writerInstance)

            for file_name in files:
                if file_name.endswith('.vm'):
                    print('writing file ending with vm: ', file_name)
                    parserInstance = Parser(file_name)
                    writerInstance = CodeWriter(file_name_to_write, output_file)
                    process_each_line(parserInstance, writerInstance)



