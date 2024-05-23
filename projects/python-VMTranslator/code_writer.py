def reset_file(file_name):
    with open(file_name, "w"):
        pass


class CodeWriter:

    def __init__(self, file_name, output_file_path):
        self.file_name = file_name
        self.capitalized_file_name = file_name.capitalize()
        self.output_file = output_file_path
        reset_file(self.output_file)
        self.SP = '@SP'
        self.new_line = '\n'
        # Below the current stack pointer
        self.set_pointer_up = '@SP\nM=M+1'
        self.set_pointer_down = '@SP\nM=M-1'
        self.push_value_of_d_to_stack = '@SP\nA=M\nM=D\n@SP\nM=M+1'
        self.set_d_to_value_at_pointer = 'A=M\nD=M'
        self.pop_stack_pointer_value_to_d = '@SP\nM=M-1\n@SP\nA=M\nD=M'
        self.address_dict = {'local': '@LCL', 'that': '@THAT', 'argument': '@ARG', 'this': '@THIS', '3': '@3',
                             '4': '@4'}
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
        self.arithmetic_operations = ['add', 'sub']
        self.logical_operations = ['gt', 'eq', 'lt', 'neg', 'not', 'or', 'and']
        self.static_counter = 0
        self.eq_loop_counter = 0
        self.lt_loop_counter = 0
        self.gt_loop_counter = 0
        self.current_this = 3
        self.current_that = 4
        self.function_name_counter_dict = {}

    def file_writer(self, code_to_write):
        with open(self.output_file, "a") as file:
            for code in code_to_write:
                file.write(code)
                file.write("\n")

    def get_push_code_line(self, arg1, arg2):
        if arg1 == 'pointer':
            if arg2 == '0':
                return ['@3', 'D=M', self.push_value_of_d_to_stack]
            elif arg2 == '1':
                return ['@4', 'D=M', self.push_value_of_d_to_stack]
            else:
                raise ValueError(f'{arg2} is not a valid number for pointer, should be either "1" or "0"')
        elif arg1 == 'static':
            target = f'@{arg1.capitalize()}.{arg2}'
            return [target, 'D=M', self.push_value_of_d_to_stack]
        if arg1 == 'temp':
            return [self.temp_dict[arg2], 'D=M', self.push_value_of_d_to_stack]
        if arg1 == 'constant':
            return ['@' + arg2, 'D=A', self.push_value_of_d_to_stack]
        if 'Static' in arg1:
            return [arg1, 'D=A', self.push_value_of_d_to_stack]
        else:
            print('PUSH ELSE', arg1, 'and', arg2)
            r_13_to_final_address = ['@' + arg2, 'D=A', self.address_dict[arg1], 'A=M', 'D=D+A', '@R13', 'M=D']
            set_final_address_to_arg2 = ['@R13', self.set_d_to_value_at_pointer, self.push_value_of_d_to_stack]
            return r_13_to_final_address + set_final_address_to_arg2

    def get_pop_temp(self, arg2):
        return [self.pop_stack_pointer_value_to_d, self.temp_dict[arg2], 'M=D']

    def get_pop_code_line(self, arg1, arg2):
        address_to_write = arg1
        if 'Static' not in arg1:
            address_to_write = self.address_dict[arg1]
        r_13_to_final_address = ['@' + arg2, 'D=A', address_to_write, 'A=M', 'D=D+A', '@R13', 'M=D']
        set_final_address_to_arg2 = [self.set_pointer_down, self.SP, self.set_d_to_value_at_pointer, '@R13', 'A=M',
                                     'M=D']
        return r_13_to_final_address + set_final_address_to_arg2

    def write_arithmetic(self, operation):
        code_to_write = []
        if operation == 'add':
            code_to_write = [
                self.pop_stack_pointer_value_to_d, self.SP,
                'A=M-1', 'M=M+D'
            ]
        elif operation == 'sub':
            code_to_write = [self.pop_stack_pointer_value_to_d, self.SP, 'A=M-1', 'M=M-D']
        self.file_writer(code_to_write)
        return

    def write_logical_operations(self, operation):
        code_to_write = []
        if operation == 'eq':
            code_to_write = [self.pop_stack_pointer_value_to_d, self.SP, 'M=M-1', 'A=M', 'D=D-M',
                             f'@EQ{self.eq_loop_counter}', 'D;JEQ', self.SP, 'A=M', 'M=0',
                             f'@EQ{self.eq_loop_counter}END',
                             '0;JMP', f'(EQ{self.eq_loop_counter})', self.SP, 'A=M', 'M=-1',
                             f'(EQ{self.eq_loop_counter}END)', self.set_pointer_up]
            self.eq_loop_counter += 1
        elif operation == 'lt':
            code_to_write = [self.pop_stack_pointer_value_to_d, self.SP, 'M=M-1', 'A=M', 'D=M-D',
                             f'@LT{self.lt_loop_counter}', 'D;JLT', self.SP, 'A=M', 'M=0',
                             f'@LT{self.lt_loop_counter}END',
                             '0;JMP', f'(LT{self.lt_loop_counter})', self.SP, 'A=M', 'M=-1',
                             f'(LT{self.lt_loop_counter}END)', self.set_pointer_up]
            self.lt_loop_counter += 1
        elif operation == 'gt':
            code_to_write = [self.pop_stack_pointer_value_to_d, self.SP, 'M=M-1', 'A=M', 'D=M-D',
                             f'@GT{self.gt_loop_counter}', 'D;JGT', self.SP, 'A=M', 'M=0',
                             f'@GT{self.gt_loop_counter}END',
                             '0;JMP', f'(GT{self.gt_loop_counter})', self.SP, 'A=M', 'M=-1',
                             f'(GT{self.gt_loop_counter}END)', self.set_pointer_up]
            self.gt_loop_counter += 1
        elif operation == 'neg':
            code_to_write = [self.SP, 'A=M-1', 'M=-M']
        elif operation == 'not':
            code_to_write = ['//NOT section', self.SP, 'A=M-1', 'M=!M']
        elif operation == 'or':
            code_to_write = [self.pop_stack_pointer_value_to_d, self.SP, 'A=M-1', 'M=D | M']
        elif operation == 'and':
            code_to_write = ['//Starting AND block', self.pop_stack_pointer_value_to_d, self.SP, 'A=M-1', 'M=D & M']
        self.file_writer(code_to_write)

    def pointer_target(self, argument_operation_number):
        target = 'this' if argument_operation_number == '0' else 'that'
        return target

    def write_push_pop(self, operation, arg1, arg2):
        code_to_write = []
        if operation == 'push':
            code_to_write = self.get_push_code_line(arg1, arg2)
        elif operation == 'pop':
            if arg1 == 'temp':
                code_to_write = self.get_pop_temp(arg2)
            elif arg1 == 'pointer':
                if arg2 == '0':
                    self.current_this = arg2
                    code_to_write = [self.pop_stack_pointer_value_to_d, '@3', 'M=D']
                elif arg2 == '1':
                    self.current_that = arg2
                    code_to_write = [self.pop_stack_pointer_value_to_d, '@4', 'M=D']
                else:
                    raise ValueError(f'{arg2} is not a valid number for pointer, should be either "1" or "0"')
            elif arg1 == 'static':
                target = f'@{arg1.capitalize()}.{arg2}'
                code_to_write = [self.pop_stack_pointer_value_to_d, target, 'M=D']
                self.static_counter += 1
                if self.static_counter >= 240:
                    raise Exception('More than 240 static variables')
            else:
                code_to_write = self.get_pop_code_line(arg1, arg2)

        self.file_writer(code_to_write)

    def create_label(self, label):
        return ["(" + label + ")"]

    def jump_conditional_if_goto_label(self, label):
        label_address = '@' + str(label)
        code_to_write = [self.pop_stack_pointer_value_to_d, '@1', 'D=D-A', label_address, 'D;JGE']
        return code_to_write

    def jump_goto_label(self, label):
        label_address = '@' + str(label)
        code_to_write = [label_address, '0;JMP']
        return code_to_write

    def function_name_counter(self, function_name):
        current_function_name = self.create_function_name(function_name)
        if current_function_name not in self.function_name_counter_dict:
            self.function_name_counter_dict[current_function_name] = 0
        else:
            self.function_name_counter_dict[current_function_name] += 1
        return self.function_name_counter_dict[current_function_name]

    def create_function_name(self, function_name):
        return self.capitalized_file_name + "." + function_name

    def create_function_label_string(self, fn_name):
        return "(" + self.capitalized_file_name + '.' + fn_name + ".$ret." + str(
            self.function_name_counter(fn_name)) + ")"

    def create_function_return_to_label(self, fn_name):
        print('counter dict', self.function_name_counter_dict)
        dict_key = self.capitalized_file_name + '.' + fn_name
        return "@" + self.capitalized_file_name + '.' + fn_name + ".$ret." + str(
            self.function_name_counter_dict[dict_key])

    def create_function_label(self, fn_name):
        return [self.create_function_label_string(fn_name)]

    def write_program_flow(self, operation, arg):
        code_to_write = []
        if operation == 'label':
            code_to_write = self.create_label(arg)
        elif operation == 'if-goto':
            code_to_write = self.jump_conditional_if_goto_label(arg)
        elif operation == 'goto':
            code_to_write = self.jump_goto_label(arg)
        self.file_writer(code_to_write)

    def create_n_vars(self, number_of_vars):
        print('number of variables', number_of_vars)
        create_vars_code = []
        for current in range(number_of_vars):
            current_lcl_count = '@' + str(current)
            create_vars_code += [current_lcl_count, 'D=A', '@LCL', 'A=D+M', 'M=0', self.set_pointer_up]
        return create_vars_code

    def create_return_function(self):
        set_temp_to_frame_from_LCL = ['@LCL', 'D=A', '@TEMP', 'M=D']
        # put return address into a temp var
        select_frame_minus_5 = ['@TEMP', 'D=A', '@5', 'D=D-A', 'A=D', 'D=M']
        put_return_address_temp_2 = ['@TEMP', 'A=A+1', 'M=D']
        # reposition return arg
        reposition_return_val = [self.pop_stack_pointer_value_to_d, '@ARG', 'A=M', 'M=D']
        # reposition SP
        reposition_sp = ['//Return function', '@ARG', 'D=M', self.SP, 'M=D+1']
        # restore caller state
        restore_that = ['@TEMP', 'D=A', '@1', 'D=D-A', '@THAT', 'A=M', 'M=D']
        restore_this = ['@TEMP', 'D=A', '@2', 'D=D-A', '@THIS', 'A=M', 'M=D']
        restore_arg = ['@TEMP', 'D=A', '@3', 'D=D-A', '@ARG', 'A=M', 'M=D']
        restore_lcl = ['@TEMP', 'D=A', '@4', 'D=D-A', '@LCL', 'A=M', 'M=D']
        goto_saved_label = ['@TEMP', 'A=A+1', 'D=A', self.SP, 'A=D']
        code_to_write = (
                    set_temp_to_frame_from_LCL + select_frame_minus_5 + put_return_address_temp_2 + reposition_return_val
                    + reposition_sp + restore_that + restore_this + restore_arg + restore_lcl + goto_saved_label)
        self.file_writer(reposition_return_val + reposition_sp)

    def create_function(self, fn_name, num_local_args):
        code_to_write = self.create_function_label(fn_name) + self.create_n_vars(int(num_local_args))
        self.file_writer(code_to_write)

    def write_code_line(self, operation, arg1=None, arg2=None):
        print('OPERATION:', operation, 'arg', arg1, 'arg2', arg2)
        if operation in self.arithmetic_operations:
            self.write_arithmetic(operation)
        elif operation in self.logical_operations:
            self.write_logical_operations(operation)
        elif operation == 'push' or operation == 'pop':
            self.write_push_pop(operation, arg1, arg2)
        elif operation == 'label' or operation == 'if-goto' or operation == 'goto':
            self.write_program_flow(operation, arg1)
        elif operation == 'function':
            self.create_function(arg1, arg2)
        elif operation == 'return':
            self.create_return_function()
