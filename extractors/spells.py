import pymupdf
import re
import json
from lib.shared import get_line_type

doc = pymupdf.open('/home/toni/Downloads/mage.pdf')
out = open("outputs/spells.txt", "wb") # create a text output

def text_from_line(line):
    full_text = ''
    for span in line['spans']:
        full_text = full_text + span['text']

    return full_text

class Spell:
    name = ''

    def __init__(self, name_line):
        self.name = text_from_line(name_line)

    def write_to_file(self, out):
        out.write(self.name.encode('utf8'))
        out.write('\n'.encode('utf8'))
        

current_spell = -1
spells = []

found_arcanum = False
found_mage_rank = False

for page_num in range(128,192): # iterate the document pages
    page = doc[page_num]
    t_page = page.get_textpage()
    # print(page)
    # print(t_page.extractDICT())
    for block in t_page.extractDICT()['blocks']:
        # skip images
        if block['type'] == 1:
            continue

        # print("Handling page %s, block %s (type=%s)" %(page_num, block['number'], block['type']))
        for line in block['lines']:

            line_type = get_line_type(line)
            if line_type != False:


                if line_type == 'spell name':
                    current_spell = current_spell + 1
                    spells.append(Spell(line))
for spell_inst in spells:
    spell_inst.write_to_file(out)

out.close()
