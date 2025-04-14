from lib.shared import get_line_type, text_from_line, tab

class Spell:
    name = ''
    practice = ''
    p_factor = ''
    spell_cost = '0'
    withstand = ''
    rote_skills = ''
    detail = ''
    arcanum_adds = ''
    reach_mods = ''

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

            case 'spell primary factor':
                self.p_factor = line_text

            case 'spell cost':
                self.spell_cost = line_text

            case 'spell withstand':
                self.withstand = line_text

            case 'spell rote skills':
                self.rote_skills = line_text

            case 'detail':
                if self.arcanum_adds == '' and self.reach_mods == '':
                    self.detail = self.detail + line_text
                elif self.reach_mods == '':
                    self.arcanum_adds = self.arcanum_adds + line_text
                else:
                    self.reach_mods = self.reach_mods + line_text

            case 'spell arcanum additions':
                self.arcanum_adds = line_text

            case 'spell reach':
                self.reach_mods = self.reach_mods + line_text

    def write_to_file(self, out):
        print(self.name)
        out.write(self.name.encode('utf8'))
        out.write(','.encode('utf8'))
        
        print("%s%s" %(tab(1), self.practice))
        out.write(self.practice.encode('utf8'))
        out.write(','.encode('utf8'))

        print("%s%s" %(tab(1), self.p_factor))
        out.write(self.p_factor.encode('utf8'))
        out.write(','.encode('utf8'))

        print("%s%s" %(tab(1), self.spell_cost))
        out.write(self.spell_cost.encode('utf8'))
        out.write(','.encode('utf8'))

        print("%s%s" %(tab(1), self.withstand))
        out.write(self.withstand.encode('utf8'))
        out.write(','.encode('utf8'))

        print("%s%s" %(tab(1), self.rote_skills))
        out.write(self.rote_skills.encode('utf8'))
        out.write(','.encode('utf8'))

        print("%s%s" %(tab(1), self.detail))
        out.write(self.detail.encode('utf8'))
        out.write(','.encode('utf8'))

        print("%s%s" %(tab(1), self.arcanum_adds))
        out.write(self.arcanum_adds.encode('utf8'))
        out.write(','.encode('utf8'))

        print("%s%s" %(tab(1), self.reach_mods))
        out.write(self.reach_mods.encode('utf8'))

        out.write('\n'.encode('utf8'))