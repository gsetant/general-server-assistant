import re

from app.plugins.adultscraperx.formatter.basicFormatter import BasicFormater


class CensoredFormatter(BasicFormater):

    def format(code):
        hCode = str(code).upper()
        if hCode[-4] == '0' and hCode[-5] == '0':
            hCode = hCode[0:-5] + hCode[-3:]

        reg_az = '\w[A-Z]+'
        results = re.findall(re.compile(reg_az), hCode)
        caz = results[0]

        reg_09 = '\d[0-9]+'
        results = re.findall(re.compile(reg_09), hCode)
        c09 = results[0]

        hCode = caz+'-'+c09
        hCode = hCode.replace('--','-')
    
    
        return hCode
