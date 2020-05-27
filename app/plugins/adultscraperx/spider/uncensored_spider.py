# -*- coding: utf-8 -*-
import logging
import sys

if sys.version.find('2', 0, 1) == 0:
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO
else:
    from io import StringIO
    from io import BytesIO

from PIL import Image

from app.plugins.adultscraperx.spider.basic_spider import BasicSpider


class UnsensoredSpider(BasicSpider):
    def poster_picture(self, url, r, w, h):
        cropped = None
        try:
            response = self.client_session.get(url)
        except Exception as ex:
            logging.info('error : %s' % repr(ex))
            return cropped

        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            # (left, upper, right, lower)

            # 制作最大尺寸背景用白色填充
            w = int(600)
            h = int(1000)
            newim = Image.new('RGB', (w, h), 'black')
            picW, picH = img.size
            newim.paste(img.resize((int(w), int(w / picW * picH))), (0, int((h - w / picW * picH) / 2)))
            cropped = newim
        else:
            pass
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
            response = self.client_session.get(url)
        except Exception as ex:
            print('error : %s' % repr(ex))
            return cropped

        img = Image.open(BytesIO(response.content))
        rimg = img.resize((200, 200), Image.ANTIALIAS)
        cropped = rimg.crop((50, 0, 150, 125))
        return cropped
