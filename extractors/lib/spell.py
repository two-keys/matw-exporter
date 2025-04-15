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

    def __init__(self, name_line):
        self.name = text_from_line(name_line)
        self.reach_mods = [] # instantiate here as instance variable

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
                if self.arcanum_adds == '' and len(self.reach_mods) == 0:
                    self.detail = self.detail + line_text
                elif len(self.reach_mods) == 0:
                    self.arcanum_adds = self.arcanum_adds + line_text
                else:
                    self.reach_mods[-1] = self.reach_mods[-1] + line_text

            case 'spell arcanum additions':
                self.arcanum_adds = line_text

            case 'spell reach':
                self.reach_mods.append(line_text)

    def write_to_file(self, out):
        data = {}

        print(self.name)
        data['Name'] = self.name
        
        print("%s%s" %(tab(1), self.practice))
        data['Practice'] = self.practice

        print("%s%s" %(tab(1), self.p_factor))
        data['Primary Factor'] = self.p_factor

        print("%s%s" %(tab(1), self.spell_cost))
        data['Spell Cost'] = self.spell_cost

        print("%s%s" %(tab(1), self.withstand))
        data['Withstand'] = self.withstand

        print("%s%s" %(tab(1), self.rote_skills))
        data['Rote Skills'] = self.rote_skills

        print("%s%s" %(tab(1), self.detail))
        data['Detail'] = self.detail

        print("%s%s" %(tab(1), self.arcanum_adds))
        data['Arcanum Adds'] = self.arcanum_adds

        print("%s%s" %(tab(1), self.reach_mods))
        data['Reach Mods'] = '\n'.join(self.reach_mods)

        out.writerow(data)