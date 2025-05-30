from lib.shared import get_line_type, text_from_line, tab
import re

class Spell:
    name = ''
    dots = 1
    arcanum = ''
    practice = ''
    p_factor = ''
    spell_cost = '0'
    withstand = ''
    rote_skills = ''
    detail = ''
    arcanum_adds = ''

    # for detail section only
    seeking = False
    last_line_was = ''

    def __init__(self, name_line):
        pattern = r"[ ]*(.*) \(([a-zA-z]+) (•+)\)"
        line_text = text_from_line(name_line)
        match = re.search(pattern, line_text)
        self.name = match.group(1)
        self.arcanum = match.group(2)
        self.dots = match.group(3)

        self.reach_mods = [] # instantiate here as instance variable

    def handle_line(self, line):
        line_type = get_line_type(line)
        line_text = text_from_line(line)

        match line_type:
            case 'spell practice':
                pattern = r"([a-zA-Z]+)$"
                match = re.search(pattern, line_text)
                self.practice = match.group(1)

            case 'spell primary factor':
                pattern = r"([a-zA-Z]+)$"
                match = re.search(pattern, line_text)
                self.p_factor = match.group(1)

            case 'spell cost':
                self.spell_cost = line_text

            case 'spell withstand':
                pattern = r"Withstand: (.*)$"
                match = re.search(pattern, line_text)
                self.withstand = match.group(1)

            case 'spell rote skills':
                self.rote_skills = line_text

            case 'detail':
                if self.rote_skills == '': # Suggested Rote Skills
                    self.withstand = self.withstand + line_text
                elif self.arcanum_adds == '' and len(self.reach_mods) == 0:
                    # didn't find either, so we're handling misc details

                    if re.match(r'^(•+.*$)', line_text):
                        real_text = re.sub(r'^(•+.*$)', r'<p>\1', line_text)
                        self.seeking = True
                        self.detail = self.detail + real_text
                    elif re.match(r'^([a-zA-Z]+:.*$)', line_text):
                        # misc detail line
                        # claws: the user can give themselves claws

                        real_text = re.sub(r'^([a-zA-Z]+:.*$)', r'<p>\1', line_text)
                        self.seeking = True
                        self.detail = self.detail + real_text
                    else:
                        self.detail = self.detail + line_text
                        if self.seeking == True:
                            self.seeking = False
                            self.detail = self.detail + '</p>'
                else:
                    match self.last_line_was:
                        case 'arcanum_add':
                            self.arcanum_adds = self.arcanum_adds + line_text
                        case 'spell_reach':
                            self.reach_mods[-1] = self.reach_mods[-1] + line_text

            case 'spell arcanum additions':
                self.arcanum_adds = self.arcanum_adds + '<p>' + line_text
                self.last_line_was = 'arcanum_add'

            case 'spell reach':
                self.reach_mods.append(line_text)
                self.last_line_was = 'spell_reach'

    def write_to_file(self, out):
        data = {}

        print("%s %s" %(self.name, self.dots))
        data['Name'] = "%s %s" %(self.name, self.dots)
        data['Dots'] = len(self.dots)

        data['Image'] = "systems/mta/icons/placeholders/%s.svg" %(self.arcanum)

        print("%s%s" %(tab(1), self.arcanum))
        data['Arcanum'] = self.arcanum.lower()
        
        print("%s%s" %(tab(1), self.practice))
        data['Practice'] = self.practice

        print("%s%s" %(tab(1), self.p_factor))
        data['Primary Factor'] = self.p_factor

        print("%s%s" %(tab(1), self.withstand))
        data['Withstand'] = self.withstand

        print("%s%s" %(tab(1), self.rote_skills))
        print("%s%s" %(tab(1), self.detail))
        data['Description'] = "<p>%s</p>"%(self.rote_skills)
        data['Description'] = data['Description'] + self.detail

        print("%s%s" %(tab(1), self.arcanum_adds))
        data['Description'] = data['Description'] + self.arcanum_adds
        
        print("%s%s" %(tab(1), self.reach_mods))
        for reach_mod in self.reach_mods:
            data['Description'] = data['Description'] + '<p>' + reach_mod

        # print("%s%s" %(tab(1), self.spell_cost))
        # data['Spell Cost'] = self.spell_cost

        out.writerow(data)