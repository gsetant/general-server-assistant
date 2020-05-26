from app.plugins.adultscraperx.formatter.basicFormatter import BasicFormater


class TenMusumeFormatter(BasicFormater):

    def format(code):
        code = code.replace('-', ' ')
        code = code.replace('_', ' ')
        if code[-3] != "-":
            if code[-3] == " ":
                return code.replace(" ", "_")
        return code