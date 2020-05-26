# -*- coding: utf-8 -*-

import re


class Tools():
    '''
    工具类
    '''

    def dict_sorted(self, dicts, orderby):
        '''
        字典排序
        <dicts>:dict
        <orderby>:asc/desc
        <return>:dict
        '''
        if orderby == 'asc':
            # 正序
            return sorted(dicts.items(), lambda x, y: cmp(x[1], y[1]))
        elif orderby == 'desc':
            # 倒序
            return sorted(dicts.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)

    def statusCodeConvert(self, code):
        '''
        服务器返回状态转换
        '''
        if code == 200:
            return u'200:服务器访问成功'
        elif code == 301:
            return u'301:服务器重定向'
        elif code == 302:
            return u'302:服务器重定向'
        elif code == 400:
            return u'400:请求无效'
        elif code == 403:
            return u'403:服务器拒绝请求'
        elif code == 404:
            return u'404:访问页面不存在'
        elif code == 502:
            return u'502:访问服务器错误'
        elif code == 504:
            return u'504:访问服务器超时'

    def cleanstr(self, st):
        st = st.replace(' ', '')
        st = st.replace('\r', '')
        st = st.replace('\n', '')
        st = st.replace('\r\n', '')
        st = st.replace(u'\xa0', '')
        st = st.replace(u'\u5ec3', '')
        st = st.replace(u'\u76e4', '')
        st = st.replace('\t','')
        return st

    def cleanstr2(self, st):
        st = st.replace('\t', '')
        st = st.replace('\r', '')
        st = st.replace('\n', '')
        st = st.replace('\r\n', '')
        st = st.replace(u'\xa0', '')
        st = st.replace(u'\u5ec3', '')
        st = st.replace(u'\u76e4', '')
        return st

    def cleanstr3(self, st):
        st = st.replace(' ', '')
        st = st.replace('\r', '')
        st = st.replace('\n', '')
        st = st.replace('\r\n', '')
        st = st.replace(u'\xa0', '')
        st = st.replace(u'\u5ec3', '')
        st = st.replace(u'\u76e4', '')
        st = st.replace(u'\u3000', '')
        return st

    def cleantitlenumber(self, st, number):
        st = st.replace(number, '')
        return st

    def formatdatetime(self, st):
        aRegex = re.compile(r'^\d{4}/\d{1,2}/\d{1,2}')
        find = aRegex.search(st)
        if not find == None:
            st = find.group()
            st = st.replace('/', '-')

        return st

    def dateconvert(self, st):
        st = st.split(',')
        if len(st)>1:
            md = st[0].split(' ')
            m = md[0].replace(' ', '')
            d = md[1].replace(' ', '')
            y = st[1].replace(' ', '')
            if m.lower() == 'Jan.'.lower() or m.lower() == 'Jan'.lower() or m.lower() == 'January'.lower():
                return '%s-1-%s' % (y, d)
            if m.lower() == 'Feb.'.lower() or m.lower() == 'Feb'.lower() or m.lower() == 'February'.lower():
                return '%s-2-%s' % (y, d)
            if m.lower() == 'Mar.'.lower() or m.lower() == 'Mar'.lower() or m.lower() == 'March'.lower():
                return '%s-3-%s' % (y, d)
            if m.lower() == 'Apr.'.lower() or m.lower() == 'Apr'.lower() or m.lower() == 'April'.lower():
                return '%s-4-%s' % (y, d)
            if m.lower() == 'May.'.lower() or m.lower() == 'May'.lower() or m.lower() == 'May'.lower():
                return '%s-5-%s' % (y, d)
            if m.lower() == 'Jun.'.lower() or m.lower() == 'Jun'.lower() or m.lower() == 'June'.lower():
                return '%s-6-%s' % (y, d)
            if m.lower() == 'Jul.'.lower() or m.lower() == 'Jul'.lower() or m.lower() == 'July'.lower():
                return '%s-7-%s' % (y, d)
            if m.lower() == 'Aug.'.lower() or m.lower() == 'Aug'.lower() or m.lower() == 'August'.lower():
                return '%s-8-%s' % (y, d)
            if m.lower() == 'Sep.'.lower() or m.lower() == 'Sep'.lower() or m.lower() == 'September'.lower():
                return '%s-9-%s' % (y, d)
            if m.lower() == 'Oct.'.lower() or m.lower() == 'Oct'.lower() or m.lower() == 'October'.lower():
                return '%s-10-%s' % (y, d)
            if m.lower() == 'Nov.'.lower() or m.lower() == 'Nov'.lower() or m.lower() == 'November'.lower():
                return '%s-11-%s' % (y, d)
            if m.lower() == 'Dec.'.lower() or m.lower() == 'Dec'.lower() or m.lower() == 'December'.lower():
                return '%s-12-%s' % (y, d)
