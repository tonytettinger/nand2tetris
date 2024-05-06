def reset_file(file_name):
    with open(file_name, "w"):
        pass


class CodeWriter:

    def __init__(self, output_file_name):
        self.output_file_name = output_file_name
        reset_file(output_file_name)
        self.SP = '@SP'
        self.new_line = '\n'
        # Below the current stack pointer
        self.get_top_value_from_stack = '@SP\nA=M-1'
        self.set_pointer_up = '@SP\nM=M+1'
        self.set_pointer_down = '@SP\nM=M-1'
        self.push_value_of_d_to_stack_pointer = '@SP\nA=M\nM=D\n@SP\nM=M+1'
        self.set_d_to_value_at_pointer = 'A=M\nD=M'
        self.pop_stack_pointer_value_to_d = '@SP\nM=M-1\n@SP\nA=M\nD=M'
        self.address_dict = {'local': '@LCL', 'that': '@THAT', 'argument': '@ARG', 'this': '@THIS'}
        self.temp_dict = {
            '0': '@5',
            '1': '@6',
            '2': '@7',
            '3': '@8',
            '4': '@9',
            '5': '@10',
            '6': '@11',
            '7': '@12'
        }

    def file_writer(self, code_to_write):
        with open(self.output_file_name, "a") as file:
            for code in code_to_write:
                file.write(code)
                file.write("\n")

    def get_push_code_line(self, arg1, arg2):
        if arg1 == 'temp':
            return [self.temp_dict[arg2], 'D=M', self.push_value_of_d_to_stack_pointer]
        if arg1 == 'constant':
            return ['@' + arg2, 'D=A', self.push_value_of_d_to_stack_pointer]
        else:
            r_13_to_final_address = ['@' + arg2, 'D=A', self.address_dict[arg1], 'A=M', 'D=D+A', '@R13', 'M=D']
            set_final_address_to_arg2 = ['@R13', self.set_d_to_value_at_pointer, self.push_value_of_d_to_stack_pointer]
            return r_13_to_final_address + set_final_address_to_arg2

    def get_pop_temp(self, arg2):
        return [self.pop_stack_pointer_value_to_d, self.temp_dict[arg2], 'M=D']

    def get_pop_code_line(self, arg1, arg2):
        r_13_to_final_address = ['@' + arg2, 'D=A', self.address_dict[arg1], 'A=M', 'D=D+A', '@R13', 'M=D']
        set_final_address_to_arg2 = [self.set_pointer_down, self.SP, self.set_d_to_value_at_pointer, '@R13', 'A=M', 'M=D']
        return r_13_to_final_address + set_final_address_to_arg2

    def write_arithmetic(self, operation):
        code_to_write = []
        if operation == 'add':
            code_to_write = [
                self.get_top_value_from_stack, 'D=M', self.set_pointer_down,
                'A=M-1', 'M=M+D'
            ]
        elif operation == 'sub':
            code_to_write = [self.get_top_value_from_stack, 'D=M', self.set_pointer_down, 'A=M-1', 'M=M-D']

        self.file_writer(code_to_write)
        return

    def write_push_pop(self, operation, arg1, arg2):
        code_to_write = []
        if operation == 'push':
            code_to_write = self.get_push_code_line(arg1, arg2)
        elif operation == 'pop':
            if arg1 == 'temp':
                code_to_write = self.get_pop_temp(arg2)
            else:
                code_to_write = self.get_pop_code_line(arg1, arg2)

        self.file_writer(code_to_write)

    def write_code_line(self, operation, arg1=None, arg2=None):
        if arg1 is None or arg2 is None:
            self.write_arithmetic(operation)
        elif operation == 'push' or operation == 'pop':
            self.write_push_pop(operation, arg1, arg2)
