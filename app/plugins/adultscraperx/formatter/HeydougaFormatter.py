import re

from app.plugins.adultscraperx.formatter.basicFormatter import BasicFormater


class HeydougaFormatter(BasicFormater):

    def format(code):
        codelist = re.findall(re.compile('\d+'), code)
        rCode = ''
        if len(codelist) >= 2:
            rCode = codelist[0]
            ppv = codelist[1]
            rCode = 'Heydouga,' + rCode + ',' + ppv
            if len(codelist) == 3:
                pt = '-PART' + codelist[2]
                rCode = rCode + pt
        return rCode
