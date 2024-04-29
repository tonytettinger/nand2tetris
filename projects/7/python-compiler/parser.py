class Parser:
    def __init__(self, file_name):
        file = open(file_name)
        self.file = file
        self.current_line = None
        self.arg1 = None
        self.arg2 = None
        self.command_type = None
        self.valid_commands = ['push', 'add']

    def has_more_lines(self):
        if self.file.closed:
            return False
        next_line = self.file.readline()
        if next_line:
            self.current_line = next_line
            return True
        else:
            self.file.close()
            return False

    def advance(self):
        if self.has_more_lines():
            if self.current_line != '\n':
                try:
                    words_of_line = self.current_line.split()
                    command = words_of_line[0]
                    if command not in self.valid_commands:
                        print('Invalid command')
                        self.command_type = None
                        raise ValueError
                    else:
                        self.command_type = command
                except ValueError:
                    print('An error occurred: invalid command')
                try:
                    if command != 'add':
                        self.arg1 = words_of_line[1]
                        self.arg2 = words_of_line[2]
                    else:
                        self.arg1 = None
                        self.arg2 = None
                except IndexError:
                    print('Missing arguments')

    def arg1(self):
        return self.arg1

    def arg2(self):
        return self.arg2

    def command_type(self):
        return self.command_type


