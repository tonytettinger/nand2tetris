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


process_dir = False

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
        directory = sys.argv[1]
        process_dir = True

if len(sys.argv) != 2:
    directory = os.getcwd()
    process_dir = True

if process_dir:
    try:
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
    output_file = file_name_to_write + ".asm"
    reset_file(output_file)

    script_directory = os.path.dirname(os.path.abspath(__file__))
    bootstrap_sys_call_file_name = 'bootstrap-sys-call.asm'
    bootstrap_initial = 'bootstrap-initial.asm'

    bootstrap_1_file_path = os.path.join(script_directory, bootstrap_initial)
    bootstrap_2_file_path = os.path.join(script_directory, bootstrap_sys_call_file_name)
    # Read the contents of the source file and write them to the destination file
    try:
        with open(bootstrap_1_file_path, 'r') as source_file_1, \
                open(bootstrap_2_file_path, 'r') as source_file_2, \
                open(output_file, 'w') as destination_file:
            destination_file.write(source_file_1.read() + '\n' + source_file_2.read())


    except FileNotFoundError:
        print(f"Error: File not found.")
    except IOError as e:
        print(f"Error: An I/O error occurred: {e}")

    # First, process the Sys.vm file if it exists
    if 'Sys.vm' in files:
        print('writing file ending with vm: Sys.vm')
        parserInstance = Parser('Sys.vm')
        writerInstance = CodeWriter('Sys', output_file)
        process_each_line(parserInstance, writerInstance)

    # Then, process all other .vm files except Sys.vm
    for file_name in files:
        if file_name.endswith('.vm') and file_name != 'Sys.vm':
            print('writing file ending with vm: ', file_name)
            file_name_without_extension = file_name.split('.')[0]
            parserInstance = Parser(file_name)
            writerInstance = CodeWriter(file_name_without_extension, output_file)
            process_each_line(parserInstance, writerInstance)
