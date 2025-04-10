def get_line_type(line):
    spns = line['spans']

    if len(spns) == 2 and spns[0]['size'] == 18.0 and spns[1]['size'] == 24.0:
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

    if len(spns) == 3 and (
            spns[0]['font'] == 'Lilith-Regular' and spns[0]['color'] == 20077 and
            spns[1]['font'] == 'ArialMT' and '\u2022' in spns[1]['text'] and spns[1]['color'] == 20077 and
            spns[2]['font'] == 'Lilith-Regular' and spns[2]['color'] == 20077
        ):
        return 'spell name'

    return False