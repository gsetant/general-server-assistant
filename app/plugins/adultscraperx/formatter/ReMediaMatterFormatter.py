from app.plugins.adultscraperx.formatter.basicFormatter import BasicFormater
import re


class ReMediaMatterFormatter(BasicFormater):

    def format(code):        
        code = code.replace(' ','')
        code = code.lower()
        re_tmp = re.findall(
            r'[a-z]{1,5}-[0-9]{1,5}', code)
        if len(re_tmp) == 1:
            return re_tmp[0]
        else:
            reCode = ReMediaMatterFormatter.reMediaName(code)
            return reCode

    def reMediaName(medianame):
        relist = []
        medianame = medianame.replace('-', ' ').replace('_', ' ').replace('.',' ')
        relist.append(r'vol[0-9]{1,3}|vol.[0-9]{1,3}|vol [0-9]{1,3}')
        relist.append(r'\(|\)|\[|\]|\{|\}|【|】')
        relist.append(r'[0-9]{1,4}x[0-9]{1,4}')
        relist.append(r'  ')
        relist.append(r':')
        relist.append(
            r'([0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2})|([0-9]{1,2} [0-9]{1,2} [0-9]{1,2})')
        relist.append(
            r'rarbg|frds|yts\.lt|yts|yts yifi|btschool|hdhome|m-team|@mteam|@HDHome')  # pt&bt
        relist.append(r'Yousei-hentai|Yousei|hentai')
        relist.append(r'18禁')
        relist.append(r'アニメ')
        relist.append(r'無修正')
        relist.append(r'高清版')
        relist.append(r'PS3')
        relist.append(r'アプコン')
        relist.append(r'HD')
        relist.append(r'GB')
        relist.append(r'\+')
        relist.append(r'BIG5')
        relist.append(r'～')
        relist.append(r'xxx')
        relist.append(r'kukas')
        relist.append(
            r'\.PROPER|\.DUPE|\.UNRATE|\.R-RATE|\.SE|\.DC|\.LIMITED|\.TS|DTS-HD|1080p|720p|BluRay|KR-OneHD|OneHD|LPCM 2 0|CNHK|1080i|MA 2\.0-DiY|[0-9]{1,2}bit')  # 标签
        relist.append(
            r'-KamiKaze|GER|VC-[0-9]|2160p|TrueHD|Audios-CMCT|Audios|CMCT| EUR| UHD| HDR|DTS-X-NIMA| 4K | 2K |WEB-DL| TJUPT| HC | HDRip|-EVO')  # 标签
        relist.append(r'\.XXX\.|\.SD\.')  # 标签
        relist.append(
            r'x26[0-9]|x\.26[0-9]|H26[0-9]|H\.26[0-9]|x\.26[0-9][a-z]|h\.26[0-9][a-z]|MPEG|MPEG[0-9]|MPEG-[0-9]|AVC|DIVX|wmv[0-9]|wma|WebM|mp4')  # 视频编码
        relist.append(
            r'AVC|ACC|AAC|AC[0-9]|AC-[0-9]|DTS|mp3|MA[0-9]\.[0-9]|')  # 音频编码
        relist.append(
            r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}$')  # 网址
        relist.append(
            r'rip|dvd|DVDrip|BDrip|HDTVRip|DVDScr|divx|Screener| TS1| VHS|VHSRip|TVRip| vcd|svcd|XviDrips|XviD|DivX|DivX[0-9]\.[0-9]{1.2}|DivX[0-9]|DivXRe-Enc|DivXRe|PDVD')  # 标记
        reg = '|'.join(relist)
        reg = reg.lower()
        re.compile(reg)
        medianame = re.sub(reg, '', medianame.lower(), flags=re.IGNORECASE)
        medianame =  medianame.replace('.', ' ').replace('com ', '').replace(' com', '').replace('  ', ' ').replace('「',' ').replace('」',' ')
        return medianame
