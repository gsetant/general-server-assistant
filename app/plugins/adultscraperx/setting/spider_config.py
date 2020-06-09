from app.plugins.adultscraperx.formatter.CaribbeanFormatter import CaribbeanFormatter
from app.plugins.adultscraperx.formatter.CaribbeancomprFormatter import CaribbeancomprFormatter
from app.plugins.adultscraperx.formatter.Fc2ClubFormatter import Fc2ClubFormatter
from app.plugins.adultscraperx.formatter.HeydougaFormatter import HeydougaFormatter
from app.plugins.adultscraperx.formatter.HeydougaOfficialFormatter import HeydougaOfficialFormatter
from app.plugins.adultscraperx.formatter.HeyzoFormatter import HeyzoFormatter
from app.plugins.adultscraperx.formatter.HeyzoOfficialFormatter import HeyzoOfficialFormatter
from app.plugins.adultscraperx.formatter.ReMediaMatterFormatter import ReMediaMatterFormatter
from app.plugins.adultscraperx.formatter.TokyoHotFormatter import TokyoHotFormatter
from app.plugins.adultscraperx.formatter.censoredFormatter import CensoredFormatter
from app.plugins.adultscraperx.formatter.data18Formatter import Data18Formatter
from app.plugins.adultscraperx.formatter.fc2ppvFormatter import Fc2ppvFormater
from app.plugins.adultscraperx.formatter.mgstageFormatter import MGStageFormatter
from app.plugins.adultscraperx.formatter.onePondoFormatter import OnePondoFormatter
from app.plugins.adultscraperx.formatter.tenMusumeFormatter import TenMusumeFormatter
from app.plugins.adultscraperx.spider.Fc2Club import Fc2Club
from app.plugins.adultscraperx.spider.HeyzoOfficial import HeyzoOfficial
from app.plugins.adultscraperx.spider.arzon import Arzon
from app.plugins.adultscraperx.spider.arzon_anime import ArzonAnime
from app.plugins.adultscraperx.spider.caribbean import Caribbean
from app.plugins.adultscraperx.spider.caribbeancompr import Caribbeancompr
from app.plugins.adultscraperx.spider.data18 import Data18
from app.plugins.adultscraperx.spider.heydougaOfficial import HeydougaOfficial
from app.plugins.adultscraperx.spider.javbus import Javbus
from app.plugins.adultscraperx.spider.javr import Javr
from app.plugins.adultscraperx.spider.mgstage import MGStage
from app.plugins.adultscraperx.spider.onePondo import OnePondo
from app.plugins.adultscraperx.spider.onejav import Onejav
from app.plugins.adultscraperx.spider.pacoPacoMama import PacoPacoMama
from app.plugins.adultscraperx.spider.tenMusume import TenMusume

SOURCE_LIST = {
    # 有码搜刮
    'censored': [
        # 常规有码影片搜刮
        {
            "name": '常规有码影片搜刮',
            "pattern": r"\w+[a-z]{1,5}\D{1}\d{1,5}|[a-z]{1,5}\d{1,5}",
            'formatter': CensoredFormatter,
            'web_list': [Arzon, Javbus, Onejav]
        },
        #  mgstage
        {
            "name": 'mgstage',
            "pattern": r"[0-9]{3}[a-z]{3,5}\D{1}\d{3,4}|[0-9]{3}[a-z]{3,4}\d{3,4}|SIRO[0-9]{3,4}|SIRO\D{1}[0-9]{4}[0-9]{3}[a-z]{3,4}\D{1}\d{3,4}|[0-9]{3}[a-z]{3,4}\d{3,4}|SIRO[0-9]{3,4}|SIRO\D{1}[0-9]{3,4}",
            'formatter': MGStageFormatter,
            'web_list': [MGStage]
        }
    ],
    # 无码搜刮
    'uncensored': [

        # Heydouga for official  4037/427   3004/q1234   ppv-051619_095   hzo-1992
        {
            "name": 'Heydouga for official',
            "pattern": r"Heydouga\D{1}[0-9]{4}\D[0-9]{1,5}|Heydouga[0-9]{4}\D[0-9]{1,5}|Heydouga\D{1}[0-9]{4}\D(Q|q)[0-9]{1,5}|Heydouga[0-9]{4}\D(Q|q)[0-9]{1,5}|Heydouga\D{1}[0-9]{4}\D(.{3})\D{1}[0-9]{4}|Heydouga[0-9]{4}\D(.{3})\D{1}[0-9]{4}|Heydouga\D{1}[0-9]{4}\D(.{3})\D[0-9]{6}\D{1}[0-9]{3}|Heydouga[0-9]{4}\D(.{3})\D[0-9]{6}\D{1}[0-9]{3}",
            'formatter': HeydougaOfficialFormatter,
            'web_list': [HeydougaOfficial]
        },
        #  javr for Heydouga
        {
            "name": 'javr for Heydouga',
            "pattern": r"(Heydouga|HEYDOUGA|heydouga).*\d+.*\d+[.*\d]{0,1}",
            'formatter': HeydougaFormatter,
            'web_list': [Javr]
        },
        # heyzo for official  1234
        {
            "name": 'heyzo for official',
            "pattern": r"hzo\D{1}[0-9]{4}|heyzo\D{1}[0-9]{4}|hzo[0-9]{4}|heyzo[0-9]{4}",
            'formatter': HeyzoOfficialFormatter,
            'web_list': [HeyzoOfficial]
        },

        # javr for  Heyzo
        {
            "name": 'javr for  Heyzo ',
            "pattern": r"(Heyzo|HEYZO|heyzo).*\d{4}",
            'formatter': HeyzoFormatter,
            'web_list': [Javr]
        },
        #   javr for TokyoHot
        {
            "name": 'javr for TokyoHot',
            "pattern": r"(tokyo|TOKYO|Tokyo).*[A-Za-z]+[\ -]?\d+",
            'formatter': TokyoHotFormatter,
            'web_list': [Javr]
        },
        #  fc2club for FC2PPV
        {
            "name": 'fc2club for FC2PPV',
            "pattern": r"(fc|Fc|FC).*\d{6,7}",
            'formatter': Fc2ClubFormatter,
            'webList': [Fc2Club]
        },
        #  javr for FC2PPV
        {
            "name": 'javr for FC2PPV',
            "pattern": r"(fc|Fc|FC).*\d{6,7}",
            'formatter': Fc2ppvFormater,
            'web_list': [Javr]
        },
        # Caribbean
        {
            "name": 'Caribbean',
            "pattern": r"\d{6}.\d{3}",
            'formatter': CaribbeanFormatter,
            'web_list': [Caribbean, Javr]
        },
        # Caribbeancompr
        {
            "name": 'Caribbeancompr',
            "pattern": r"\d{6}.\d{3}",
            'formatter': CaribbeancomprFormatter,
            'web_list': [Caribbeancompr, Javr]
        },
        # Pacopacomama
        {
            "name": 'Pacopacomama',
            "pattern": r"\d{6}.\d{3}",
            'formatter': OnePondoFormatter,
            'web_list': [PacoPacoMama, Javr]
        },
        # 10musume
        {
            "name": '10musume',
            "pattern": r"\d{6}.\d{2}",
            'formatter': TenMusumeFormatter,
            'web_list': [TenMusume, Javr]
        },
        # one_pondo
        {
            "name": 'one_pondo',
            "pattern": r"\d{6}.\d{3}",
            'formatter': OnePondoFormatter,
            'web_list': [OnePondo, Javr]
        }

    ],

    # 动漫搜刮
    'animation': [
        {
            "name": '动漫搜刮',
            'pattern': r'[a-z]{1,5}\D{1}[0-9]{1,5}|[a-z]{1,5}[0-9]{1,5}',
            'formatter': ReMediaMatterFormatter,
            'web_list': [ArzonAnime]
        }
    ],

    # 欧美搜刮
    'europe': [
        {
            "name": '欧美搜刮',
            "pattern": ".+",
            'formatter': Data18Formatter,
            'web_list': [Data18]
        }
    ]
}
