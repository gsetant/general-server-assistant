import re

from app.plugins.adultscraperx.formatter.basicFormatter import BasicFormater


class Fc2ppvFormater(BasicFormater):

    def format(code):
        rCode = ''
        codeList = re.findall(re.compile('\d{6,7}'), code)
        if len(codeList) == 1:
            rCode = 'fc2,ppv,' + codeList[0]
        return rCode
