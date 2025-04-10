def get_line_type(line):
    if len(line['spans']) == 2 and line['spans'][0]['size'] and line['spans'][1]['size']:
        return 'mage rank'

    if len(line['spans']) == 1 and line['spans'][0]['font'] == 'VTCGoblinHandBold-SC700' and line['spans'][0]['color'] == 4094872:
        return 'page'


    return False