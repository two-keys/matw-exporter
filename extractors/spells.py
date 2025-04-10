import pymupdf
import re
import json
from lib.shared import get_line_type, text_from_line
from lib.spell import Spell

doc = pymupdf.open('/home/toni/Downloads/mage.pdf')
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
            # initialize 
            if line_type == 'spell name':
                current_spell = current_spell + 1
                spells.append(Spell())
            
            # offload handling to Spell class
            if len(spells) > 0:
                spells[current_spell].handle_line(line)
for spell_inst in spells:
    spell_inst.write_to_file(out)

out.close()
