from app.plugins.adultscraperx.formatter.basicFormatter import BasicFormater


class OnePondoFormatter(BasicFormater):

    def format(code):
        code = code.replace('-', ' ')
        code = code.replace('_', ' ')
        if code[-4] != "-":
            if code[-4] == " ":
                return code.replace(" ", "_")
        return code