import pymupdf
import re

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

arcanum = ''
found_rank = False

spell_piece_count = 0
spell_pieces = []
current_spell = ''

is_reach = False
is_add = False

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
            for span in line['spans']:
                span_type = font_map[span['font']] if span['font'] in font_map else span['font']
                color = span['color']
                text = span['text']
                size = span['size']

                if not skippable(span):
                    console_text = "%s | type(%s), color(%s), size(%s)" %(text, span_type, color, size)
                    # print(console_text)

                    # note when we found arcanum
                    if span_type == 'arcanum' and color == 20077:
                        print("Found arcanum section %s" %(text))
                        arcanum = text
                        found_rank = True # we can skip preamble

                    if ((span_type == 'spell' and ('(' in text or ')' in text)) or span_type == 'dots') and color == 20077:
                        spell_piece_count = spell_piece_count + 1
                        spell_pieces.append(text)
                        if spell_piece_count == 3:
                            # print result
                            current_spell = ''.join(spell_pieces)
                            print(current_spell + '\n')

                            # reset spell
                            spell_piece_count = 0
                            spell_pieces = []

                    # handle header spans
                    if span_type == 'misc_heading' and color == 0:

                        is_reach = False
                        is_add = False
                        if re.search("^Add [a-zA-z]+$", text):
                            last_heading = "%s:" %(text)
                            print(last_heading)
                            is_add = True
                        elif re.search("^\+[0-9] Reach$", text): # reach
                            last_heading = text
                            print(last_heading)
                            is_reach = True
                        else:
                            last_heading = text
                            print(last_heading)

                    # handle misc_detail spans
                    if span_type == 'misc_detail' and color == 0:
                        last_heading = text
                        print(last_heading)

                    writeable_text = "%s %s" %(console_text, '\n')
                    out.write(writeable_text.encode("utf8")) # write text of page
                    # out.write(bytes((12,))) # write page delimiter (form feed 0x0C)
    text = page.get_text('json').encode("utf8") # get plain text (is in UTF-8)
out.close()
