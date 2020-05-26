import re

from app.plugins.adultscraperx.formatter.basicFormatter import BasicFormater


class HeyzoOfficialFormatter(BasicFormater):

    def format(code):
        codes = re.finditer(r'[0-9]{4}', code)
        for item in codes:
            code = item.group()
        code = 'heyzo-%s' % code
        return code
