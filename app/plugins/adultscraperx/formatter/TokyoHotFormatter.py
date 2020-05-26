import re

from app.plugins.adultscraperx.formatter.basicFormatter import BasicFormater


class TokyoHotFormatter(BasicFormater):

    def format(code):
        rCode = ''
        codelist = re.findall(re.compile('[A-Za-z]+[\ -]?\d+'), code)
        if len(codelist) == 1:
            rCode = 'Tokyo,Hot,'+codelist[0]
        return rCode
