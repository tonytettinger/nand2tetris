class Parser:
    def __init__(self, file_name):
        file = open(file_name)
        self.file = file
        self.current_line = None
        self.arg1 = None
        self.arg2 = None
        self.valid_commands = ['push', 'add']

    def has_more_lines(self):
        next_line = self.file.readline()
        if next_line:
            self.current_line = next_line
            return True
        else:
            print('else')
            return False

    def advance(self):
        if self.has_more_lines():
            if self.current_line != '\n':
                try:
                    words_of_line = self.current_line.split()
                    command = words_of_line[0]
                    if command not in self.valid_commands:
                        raise Exception('Invalid command')
                except Exception as error:
                    print('An error occurred: ', error)
                try:
                    if command != 'add':
                        self.arg1 = words_of_line[1]
                        self.arg2 = words_of_line[2]
                except:
                    print('An error occurred: ', 'Missing arguments')

    def arg1(self):
        return self.arg1

    def arg2(self):
        return self.arg2



