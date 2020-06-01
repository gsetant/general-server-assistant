import base64
import logging
from io import BytesIO
from lxml import etree  # Xpath包

from PIL import Image

import requests

from app.plugins.adultscraperx.setting import config
from app.plugins.adultscraperx.internel.config import ConfigManager
from app.plugins.adultscraperx.internel.tools import Tools
from app.tools.cache_tools import check_cache, set_cache


class BasicSpider:

    def __init__(self):
        self.tools = Tools()
        self.config_manager = ConfigManager()
        self.client_session = requests.Session()
        self.checkUrl = ''  # 服务状态检查Url 子类必须为此变量赋值

    def search_with_img(self, q):
        """
        搜索并获取图片
        :param q:
        :return:
        """
        media_infos = self.search(q)
        for media_info in media_infos:
            self.picture_processing(media_info)
        return media_infos

    def search(self, q):
        """
        根据番号爬取数据（子类必须实现）
        :param q: 番号
        :return:  json格式的数据plex直接使用
        """
        raise RuntimeError('未实现接口')

    def analysis_media_html_byxpath(self, html, q):
        """
       根据爬取的数据格式化为plex能使用的数据（子类必须实现，供search（q）方法使用的工具方法）
       :param html: 番号
       :param q: 番号
       :return:  格式化后的网站数据，可被plex使用
       """
        raise RuntimeError('未实现接口')

    def poster_picture(self, url, r, w, h):
        """
       处理海报图片，默认实现根据webui配置进行剪裁，如果子类无特殊需求不需要重写
       :param url: 图片地址
       :param r: 横向裁切位置
       :param w: 缩放比例:宽
       :param h: 缩放比例:高
       :return: 处理后的图片
       """
        cropped = None
        try:
            response = requests.get(url)
            if response.status_code == 403:
                response = self.client_session.get(url)

        except Exception as ex:
            print('error : %s' % repr(ex))
            return cropped

        img = Image.open(BytesIO(response.content))
        rims = img.resize((int(w), int(h)), Image.ANTIALIAS)
        # (left, upper, right, lower)
        cropped = rims.crop((int(w) - int(r), 0, int(w), int(h)))
        return cropped

    def art_picture(self, url, r, w, h):
        cropped = None
        """
        处理背景图片，默认实现不进行剪裁，如果子类无特殊需求不需要重写
        :param url: 图片地址
        :param r: 横向裁切位置
        :param w: 缩放比例:宽
        :param h: 缩放比例:高
        :return: 处理后的图片
        """
        cropped = None
        try:
            response = requests.get(url)
            if response.status_code == 403:
                response = self.client_session.get(url)
        except Exception as ex:
            print('error : %s' % repr(ex))
            return cropped
        img = Image.open(BytesIO(response.content))
        cropped = img.crop((0, 0, img.size[0], img.size[1]))

        return cropped

    def actor_picture(self, url, r, w, h):
        """
       处理艺人图片，默认实现根据webui配置进行剪裁，如果子类无特殊需求不需要重写
       :param url: 图片地址
       :param r: 横向裁切位置
       :param w: 缩放比例:宽
       :param h: 缩放比例:高
       :return: 处理后的图片
       """
        cropped = None
        try:
            response = requests.get(url)
            if response.status_code == 403:
                response = self.client_session.get(url)
        except Exception as ex:
            print('error : %s' % repr(ex))
            return cropped

        img = Image.open(BytesIO(response.content))
        rimg = img.resize((int(w), int(h)), Image.ANTIALIAS)
        # (left, upper, right, lower)
        cropped = rimg.crop((int(w) - int(r), 0, int(w), int(h)))
        # TODO 目前除Arzon实现了演员图片外其他站未实现，且默认实现未提供
        return cropped

    def get_name(self):
        return self.__class__.__name__

    def picture_to_base64 (self, img):
        output_buffer = BytesIO()
        img.save(output_buffer, format='JPEG')
        byte_data = output_buffer.getvalue()
        base64_str = base64.b64encode(byte_data)
        return base64_str.decode("utf-8")

    def picture_processing(self, media_info):
        r = config.IMG_R
        w = config.IMG_W
        h = config.IMG_H
        cropped = None
        # 开始剪切
        if media_info.poster:
            media_info.poster = self.picture_to_base64(self.poster_picture(media_info.poster, r, w, h))
        if media_info.thumbnail:
            media_info.thumbnail = self.picture_to_base64(self.art_picture(media_info.thumbnail, r, w, h))
        if media_info.actor:
            for (k, v) in media_info.actor.items():
                if v:
                    media_info.actor[k] = self.picture_to_base64(self.actor_picture(v, r, w, h))

    def web_site_confirm_by_url(self, url, headers):
        '''
        针对有需要确认访问声明的站点
        return: <dict{issuccess,ex}>
        '''
        item = {
            'issuccess': False,
            'ex': None
        }
        self.client_session.headers = headers
        try:
            self.client_session.get(
                url, allow_redirects=False)
        except requests.RequestException as e:
            item.update({'issuccess': False, 'ex': e})

        item.update({'issuccess': True, 'ex': None})
        return item

    def getimage(self, url):
        try:
            r = self.client_session.get(url)
        except requests.RequestException as e:

            return r.content

    def get_html_byurl(self, url):
        '''
        获取html对象函数
        url：需要访问的地址<str>
        return:<dict{issuccess,ex,html}>
        '''
        html = None
        item = {'issuccess': False, 'html': None, 'ex': None}
        try:
            r = self.client_session.get(url, allow_redirects=False)
        except requests.RequestException as e:
            item.update({'issuccess': False, 'html': None, 'ex': e})
            return item

        r.encoding = r.apparent_encoding
        if r.status_code == 200:
            t = r.text.replace('\r', '').replace(
                '\n', '').replace('\r\n', '')
            t = t.replace('<?xml version="1.0" encoding="UTF-8"?>', '')
            t = t.replace(
                '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"', '')
            t = t.replace(
                '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">', '')

            html = etree.HTML(t)
            item.update({'issuccess': True, 'html': html, 'ex': None})
        else:
            scc = self.tools.statusCodeConvert(r.status_code)
            logging.info('匹配数据结果：%s' % scc)
            item.update({'issuccess': False, 'html': None,
                         'execpt': scc})
        return item

    def get_html_byurlheaders(self, url, headers):
        """
        获取html对象函数
        url：需要访问的地址<str>
        return:<dict{issuccess,ex,html}>
        """
        html = None
        item = {'issuccess': False, 'html': None, 'ex': None}
        try:
            self.client_session.headers = headers
            r = self.client_session.get(url, allow_redirects=False)
        except requests.RequestException as e:
            item.update({'issuccess': False, 'html': None, 'ex': e})
            return item

        r.encoding = r.apparent_encoding
        if r.status_code == 200:
            t = r.text.replace('\r', '').replace(
                '\n', '').replace('\r\n', '')
            t = t.replace('<?xml version="1.0" encoding="UTF-8"?>', '')
            t = t.replace(
                '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"', '')
            t = t.replace(
                '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">', '')

            html = etree.HTML(t)
            item.update({'issuccess': True, 'html': html, 'ex': None})
        else:
            scc = self.tools.statusCodeConvert(r.status_code)
            item.update({'issuccess': False, 'html': None,
                         'execpt': scc})
        return item

    def getitemspage(self, html, xpaths):
        url = html.xpath(xpaths)
        return url

    def check_server(self):
        """
        检测站点是否在线
        :return: 站点是否在线
        """
        html_item = self.get_html_byurl(self.checkUrl)
        if html_item['issuccess']:
            return True
        else:
            return False
