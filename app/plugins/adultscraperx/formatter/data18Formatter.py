import re

from app.plugins.adultscraperx.formatter.ReMediaMatterFormatter import ReMediaMatterFormatter


class Data18Formatter(ReMediaMatterFormatter):

    def format(code):
        reCode = ReMediaMatterFormatter.reMediaName(code)
        reg = r'(?i)vol[0-9]{1,3}'
        re.compile(reg)
        reCode = re.sub(reg, '', reCode)
        return reCode
