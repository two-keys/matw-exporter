import pymupdf
import re
import json

doc = pymupdf.open('/home/toni/Downloads/mage.pdf')
out = open("outputs/spells.txt", "wb") # create a text output

font_map = {
    'VTCGoblinHandBold-SC700': 'page',
    'VTCGoblinHandBold': 'arcanum',
    'Arial-Black': 'mage_rank',
    'FuturaT-Bold': 'sympathy_header',
    'DeadHistory': 'prose_title',
    'FuturaT-Book': 'prose',
    'Lilith-Regular': 'spell',
    'ArialMT': 'dots',
    'GoudyOldStyleT-Bold': 'misc_heading',
    'GoudyOldStyleT-Regular': 'misc_detail',
    'GoudyOldStyleT-Italic': 'misc_detail' # italics
}

def skippable(span):
    # initialize variables
    span_type = font_map[span['font']] if span['font'] in font_map else span['font']
    color = span['color']
    text = span['text']

    is_skippable = False

    # page number
    is_skippable = True if color == 4094872 and span_type == 'page' else is_skippable
    # page arcanum footer
    is_skippable = True if color == 4094872 and span_type == 'arcanum' else is_skippable

    # colon for Add <Arcanum>
    is_skippable = True if (':' in text and span_type == 'misc_heading') else is_skippable

    # chapter title
    is_skippable = True if color == 23931 and span_type == 'arcanum' else is_skippable

    # blue text boxes titles
    is_skippable = True if color == 20077 and span_type == 'prose_title' else is_skippable

    # blue text boxes content
    is_skippable = True if color == 20077 and span_type == 'prose' else is_skippable

    # 

    return is_skippable

current_spell = ''

spells = {}

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
            full_text = ''
            for span in line['spans']:
                full_text = full_text + span['text']
            if re.search("^.* \([a-zA-Z]+ •+\)$", full_text): # get spell name
                if current_spell != '': # dont print on first loop
                    print(spells[current_spell])
                    out.write(json.dumps(spells[current_spell]).encode('utf8')) # write text of page
                    out.write('\n'.encode('utf8')) # write text of page
                current_spell = full_text
                spells[current_spell] = { "details": '' }
            elif current_spell in spells.keys():
                spells[current_spell]['details'] = spells[current_spell]['details'] + full_text + '\n'
    text = page.get_text('json').encode("utf8") # get plain text (is in UTF-8)
out.close()
