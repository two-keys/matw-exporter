import re

def get_line_type(line):
    spns = line['spans']

    if len(spns) == 2 and (spns[0]['size'] == 18.0 or spns[0]['text'] == '\u2022') and spns[1]['size'] == 24.0:
        return 'mage rank'

    if len(spns) == 1 and spns[0]['font'] == 'VTCGoblinHandBold-SC700' and spns[0]['color'] == 4094872:
        return 'footer page'

    if len(spns) == 1 and (
            spns[0]['font'] == 'VTCGoblinHandBold' and spns[0]['size'] == 11.0 and
            spns[0]['color'] == 4094872
        ):
        return 'footer arcanum'

    if len(spns) == 1 and spns[0]['text'] == 'chapter four: magic':
        return 'footer chapter'

    if len(spns) == 1 and spns[0]['size'] == 33.0:
        return 'large arcanum'

    if len(spns) == 2 and spns[0]['text'] == 'Purview:':
        return 'arcanum purview'

    if len(spns) == 1 and (
            spns[0]['font'] == 'Lilith-Regular' and spns[0]['size'] == 19.0
            and spns[0]['color'] == 20077
        ) or (
            spns[0]['font'] == 'DeadHistory' and spns[0]['size'] == 14.0
        ):
        return 'blurb title'

    if len(spns) == 1 and (
            spns[0]['font'] == 'FuturaT-Bold' and spns[0]['size'] == 9.899495124816895
            and spns[0]['color'] == 20077
        ) or (
            spns[0]['font'] == 'FuturaT-Book' and (spns[0]['size'] in [11.0, 9.899495124816895])
            and spns[0]['color'] == 20077
        ):
        return 'blurb misc'

    if len(spns) == 3 and (
            spns[0]['font'] == 'Lilith-Regular' and spns[0]['color'] in [20077, 16734] and
            spns[1]['font'] in ['ArialMT', 'Arial-Black'] and '\u2022' in spns[1]['text']
                and spns[1]['color'] in [20077, 16734] and
            spns[2]['font'] == 'Lilith-Regular' and spns[2]['color'] in [20077, 16734]
        ):
        return 'spell name'

    if len(spns) >= 1 and (
            spns[0]['font'] == 'GoudyOldStyleT-Bold' and spns[0]['color'] == 0 and
            re.search("^Practice:", spns[0]['text'])
        ):
        return 'spell practice'

    if len(spns) == 2 and (
            spns[0]['font'] == 'GoudyOldStyleT-Bold' and spns[0]['color'] == 0 and
            re.search("^Primary (Spell )?Factor:", spns[0]['text'])
        ):
        return 'spell primary factor'

    if len(spns) >= 2 and (
            spns[0]['font'] == 'GoudyOldStyleT-Bold' and spns[0]['color'] == 0 and
            'Suggested Rote Skills:' in spns[0]['text']
        ):
        return 'spell rote skills'

    if len(spns) == 2 and (
            spns[0]['font'] == 'GoudyOldStyleT-Bold' and spns[0]['color'] == 0 and
            'Withstand:' in spns[0]['text']
        ):
        return 'spell withstand'

    if len(spns) == 1 and (
        spns[0]['font'] == 'GoudyOldStyleT-Regular' and spns[0]['color'] == 0 and
        re.search("^Withstand: Hallow Rating", spns[0]['text'])
    ):
        return 'spell withstand'

    if len(spns) == 2 and (
        spns[0]['font'] == 'GoudyOldStyleT-Bold' and spns[0]['color'] == 0 and
        re.search("^Cost:", spns[0]['text'])
    ):
        return 'spell cost'

    if len(spns) >= 2 and (
        re.search("^\+[ ]?[0-9] Reach", spns[0]['text'])
    ):
        return 'spell reach'

    if len(spns) >= 1 and (
        (
            spns[0]['font'] == 'GoudyOldStyleT-Bold' or 
            spns[0]['font'] == 'GoudyOldStyleT-Regular' 
        ) and 
        spns[0]['color'] == 0 and
        re.search("^Add \w+", spns[0]['text'])
    ):
        return 'spell arcanum additions'

    if len(spns) >= 1 and (
        spns[0]['font'] == 'GoudyOldStyleT-Regular'
        and spns[0]['size'] == 10.0 and spns[0]['color'] == 0
    ):
        return 'detail'

    return 'detail'

    return False

def text_from_line(line):
    full_text = ''
    for span in line['spans']:
        full_text = full_text + span['text']

    return full_text

def tab(count):
    tabs = ''
    for i in range(count):
        tabs = tabs + '\t'
    return tabs