import re

from app.plugins.adultscraperx.formatter.basicFormatter import BasicFormater


class HeyzoFormatter(BasicFormater):

    def format(code):
        rCode = ''
        codelist = re.findall(re.compile('\d{4}'), code)
        if len(codelist) == 1:
            rCode = 'Heyzo,' + codelist[0]
        return rCode
