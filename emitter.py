class Emitter:
    def __init__ (self, file_path):
        self.file_path = file_path
        self.header = ""
        self.code = ""

    def emit (self, code):
        self.code += code

    def emit_line(self, line):
        self.code += (line + '\n')

    def header_line(self, line):
        self.header += (line + '\n')

    def write_file(self):
        with open(self.file_path, 'w') as output_file:
            output_file.write(self.header + self.code)
            


