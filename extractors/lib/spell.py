from lib.shared import get_line_type, text_from_line

class Spell:
    name = ''

    def __init__(self, name_line):
        self.name = text_from_line(name_line)

    def write_to_file(self, out):
        out.write(self.name.encode('utf8'))
        out.write('\n'.encode('utf8'))