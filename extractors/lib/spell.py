from lib.shared import get_line_type, text_from_line, tab

class Spell:
    name = ''
    practice = ''

    def __init__(self, name_line):
        self.name = text_from_line(name_line)

    def handle_line(self, line):
        line_type = get_line_type(line)
        line_text = text_from_line(line)

        match line_type:
            case 'spell name':
                self.name = line_text

            case 'spell practice':
                self.practice = line_text

    def write_to_file(self, out):
        print(self.name)
        out.write(self.name.encode('utf8'))
        out.write(','.encode('utf8'))
        
        print("%s%s" %(tab(1), self.practice))
        out.write(self.practice.encode('utf8'))
        out.write('\n'.encode('utf8'))