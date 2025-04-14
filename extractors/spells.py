import pymupdf
import re
import json
from lib.shared import get_line_type, text_from_line
from lib.spell import Spell

doc = pymupdf.open('pdf/mage.pdf')
out = open("outputs/spells.txt", "wb") # create a text output

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
            match line_type:
                case 'spell name':
                    # initialize 
                    current_spell = current_spell + 1
                    spells.append(Spell(line))
                    # print(text_from_line(line))
                case 'large arcanum':
                    found_arcanum = True
                    found_mage_rank = False

                    # print(text_from_line(line))
                case 'mage rank':
                    if re.search("[ ]?Initiate of", text_from_line(line)):
                        found_mage_rank = True
                case _:
                    # skip arcanum flavor text
                    if found_mage_rank:
                        # offload handling to Spell class
                        spells[current_spell].handle_line(line)
for spell_inst in spells:
    spell_inst.write_to_file(out)

out.close()
