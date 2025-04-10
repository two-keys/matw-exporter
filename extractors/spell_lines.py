import pymupdf
import re
import json
from lib.shared import get_line_type

doc = pymupdf.open('/home/toni/Downloads/mage.pdf')
out = open("outputs/spells.txt", "wb") # create a text output

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
            debug_line = "line | %s \n" %(line_type)
            out.write(debug_line.encode('utf8'))

            for span in line['spans']:
                out.write('\t'.encode('utf8'))
                out.write(json.dumps(span).encode('utf8'))
                out.write('\n'.encode('utf8')) # write text of page
    text = page.get_text('json').encode("utf8") # get plain text (is in UTF-8)
out.close()
