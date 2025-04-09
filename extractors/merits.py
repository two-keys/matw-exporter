import pymupdf

doc = pymupdf.open('/home/toni/Downloads/mage.pdf')
out = open("outputs/mage_merits.txt", "wb") # create a text output

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

for page_num in range(185,192): # iterate the document pages
    page = doc[page_num]
    t_page = page.get_textpage()
    print(page)
    # print(t_page.extractDICT())
    for block in t_page.extractDICT()['blocks']:
        # skip images
        if block['type'] == 1:
            continue

        print("Handling page %s, block %s (type=%s)" %(page_num, block['number'], block['type']))
        for line in block['lines']:
            for span in line['spans']:
                span_type = font_map[span['font']] if span['font'] in font_map else span['font']
                text = span['text']             

                console_text = "%s | %s" %(text, span_type)
                print(console_text)

                writeable_text = "%s %s" %(console_text, '\n')
                out.write(writeable_text.encode("utf8")) # write text of page
                # out.write(bytes((12,))) # write page delimiter (form feed 0x0C)
    text = page.get_text('json').encode("utf8") # get plain text (is in UTF-8)
out.close()
