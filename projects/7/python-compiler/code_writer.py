def reset_file():
    with open("SimpleAdd.asm", "w"):
        pass


def file_writer(code_to_write):
    with open("SimpleAdd.asm", "a") as file:
        for code in code_to_write:
            file.write(code)
            file.write("\n")


class CodeWriter:

    def __init__(self):
        reset_file()
        self.SP = '@SP'
        self.new_line = '\n'
        # Below the current stack pointer
        self.get_top_value_from_stack = '@SP\nA=M-1'
        self.set_pointer_up = '@SP\nM=M+1'
        self.set_pointer_down = '@SP\nM=M-1'
        self.set_pointer_val_d = '@SP\nA=M\nM=D'

    def write_arithmetic(self, operation):
        code_to_write = []
        if operation == 'add':
            code_to_write = [
                self.get_top_value_from_stack, 'D=M', self.set_pointer_down,
                'A=M-1', 'M=M+D'
            ]
        file_writer(code_to_write)

    def write_push_pop(self, operation, arg1, arg2):
        code_to_write = []
        if operation == 'push':
            if arg1 == 'constant':
                code_to_write = ['@' + arg2, 'D=A', self.set_pointer_val_d, self.set_pointer_up]

            # if operation == 'pop':
            #     '@SP\nA=M-1\nD=M\n@SP\nM=M-1'

        file_writer(code_to_write)
