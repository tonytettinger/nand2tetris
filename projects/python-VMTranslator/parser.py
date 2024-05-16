class Parser:
    def __init__(self, file_name):
        file = open(file_name)
        self.file = file
        self.current_line = None
        self.arg1 = None
        self.arg2 = None
        self.command_type = None
        self.valid_commands = ['push', 'add', 'pop', 'sub', 'lt', 'gt', 'eq', 'and', 'not', 'or', 'neg', 'label','if-goto', 'goto']

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
            while self.current_line == '\n' or self.current_line.split()[0] == '//':
                self.has_more_lines()
            try:
                words_of_line = self.current_line.split()
                command = words_of_line[0]
                if command not in self.valid_commands:
                    self.command_type = None
                    raise ValueError
                else:
                    self.command_type = command
            except ValueError:
                print('An error occurred: invalid command: ', command)
            try:
                self.arg1 = None
                self.arg2 = None
                if command == 'push' or command == 'pop':
                    self.arg1 = words_of_line[1]
                    self.arg2 = words_of_line[2]

                elif command == 'if-goto' or command == 'label':
                    self.arg1 = words_of_line[1]

                return True
            except IndexError:
                print('Missing arguments')

    def arg1(self):
        return self.arg1

    def arg2(self):
        return self.arg2

    def command_type(self):
        return self.command_type


