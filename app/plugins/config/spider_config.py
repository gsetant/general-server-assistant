from app.formatter.CaribbeanFormatter import CaribbeanFormatter
from app.formatter.CaribbeancomprFormatter import CaribbeancomprFormatter
from app.formatter.HeydougaFormatter import HeydougaFormatter
from app.formatter.HeydougaOfficialFormatter import HeydougaOfficialFormatter
from app.formatter.HeyzoFormatter import HeyzoFormatter
from app.formatter.HeyzoOfficialFormatter import HeyzoOfficialFormatter
from app.formatter.ReMediaMatterFormatter import ReMediaMatterFormatter
from app.formatter.TokyoHotFormatter import TokyoHotFormatter
from app.formatter.censoredFormatter import CensoredFormatter
from app.formatter.data18Formatter import Data18Formatter
from app.formatter.fc2ppvFormatter import Fc2ppvFormater
from app.formatter.mgstageFormatter import MGStageFormatter
from app.formatter.onePondoFormatter import OnePondoFormatter
from app.formatter.tenMusumeFormatter import TenMusumeFormatter
from app.spider.HeyzoOfficial import HeyzoOfficial
from app.spider.arzon import Arzon
from app.spider.arzon_anime import ArzonAnime
from app.spider.caribbean import Caribbean
from app.spider.caribbeancompr import Caribbeancompr
from app.spider.data18 import Data18
from app.spider.heydougaOfficial import HeydougaOfficial
from app.spider.javbus import Javbus
from app.spider.javr import Javr
from app.spider.mgstage import MGStage
from app.spider.onePondo import OnePondo
from app.spider.onejav import Onejav
from app.spider.pacoPacoMama import PacoPacoMama
from app.spider.tenMusume import TenMusume

SOURCE_LIST = {
    # 有码搜刮
    'censored': [
        # 常规有码影片搜刮
        {
            "name": '常规有码影片搜刮',
            "pattern": r"\w+[a-z]{1,5}\D{1}\d{1,5}|[a-z]{1,5}\d{1,5}",
            'formatter': CensoredFormatter,
            'webList': [Arzon, Javbus, Onejav]
        },
        #  mgstage
        {
            "name": 'mgstage',
            "pattern": r"[0-9]{3}[a-z]{3,5}\D{1}\d{3,4}|[0-9]{3}[a-z]{3,4}\d{3,4}|SIRO[0-9]{3,4}|SIRO\D{1}[0-9]{4}[0-9]{3}[a-z]{3,4}\D{1}\d{3,4}|[0-9]{3}[a-z]{3,4}\d{3,4}|SIRO[0-9]{3,4}|SIRO\D{1}[0-9]{3,4}",
            'formatter': MGStageFormatter,
            'webList': [MGStage]
        }
    ],
    # 无码搜刮
    'uncensored': [

        # Heydouga for official  4037/427   3004/q1234   ppv-051619_095   hzo-1992
        {
            "name": 'Heydouga for official',
            "pattern": r"Heydouga\D{1}[0-9]{4}\D[0-9]{1,5}|Heydouga[0-9]{4}\D[0-9]{1,5}|Heydouga\D{1}[0-9]{4}\D(Q|q)[0-9]{1,5}|Heydouga[0-9]{4}\D(Q|q)[0-9]{1,5}|Heydouga\D{1}[0-9]{4}\D(.{3})\D{1}[0-9]{4}|Heydouga[0-9]{4}\D(.{3})\D{1}[0-9]{4}|Heydouga\D{1}[0-9]{4}\D(.{3})\D[0-9]{6}\D{1}[0-9]{3}|Heydouga[0-9]{4}\D(.{3})\D[0-9]{6}\D{1}[0-9]{3}",
            'formatter': HeydougaOfficialFormatter,
            'webList': [HeydougaOfficial]
        },
        #  javr for Heydouga
        {
            "name": 'javr for Heydouga',
            "pattern": r"(Heydouga|HEYDOUGA|heydouga).*\d+.*\d+[.*\d]{0,1}",
            'formatter': HeydougaFormatter,
            'webList': [Javr]
        },
        # heyzo for official  1234
        {
            "name": 'heyzo for official',
            "pattern": r"hzo\D{1}[0-9]{4}|heyzo\D{1}[0-9]{4}|hzo[0-9]{4}|heyzo[0-9]{4}",
            'formatter': HeyzoOfficialFormatter,
            'webList': [HeyzoOfficial]
        },

        # javr for  Heyzo
        {
            "name": 'javr for  Heyzo ',
            "pattern": r"(Heyzo|HEYZO|heyzo).*\d{4}",
            'formatter': HeyzoFormatter,
            'webList': [Javr]
        },
        #   javr for TokyoHot
        {
            "name": 'javr for TokyoHot',
            "pattern": r"(tokyo|TOKYO|Tokyo).*[A-Za-z]+[\ -]?\d+",
            'formatter': TokyoHotFormatter,
            'webList': [Javr]
        },
        #  javr for FC2PPV
        {
            "name": 'javr for FC2PPV',
            "pattern": r"(fc|Fc|FC).*\d{6,7}",
            'formatter': Fc2ppvFormater,
            'webList': [Javr]
        },
        # Caribbean
        {
            "name": 'Caribbean',
            "pattern": r"\d{6}.\d{3}",
            'formatter': CaribbeanFormatter,
            'webList': [Caribbean, Javr]
        },
        # Caribbeancompr
        {
            "name": 'Caribbeancompr',
            "pattern": r"\d{6}.\d{3}",
            'formatter': CaribbeancomprFormatter,
            'webList': [Caribbeancompr, Javr]
        },
        # Pacopacomama
        {
            "name": 'Pacopacomama',
            "pattern": r"\d{6}.\d{3}",
            'formatter': OnePondoFormatter,
            'webList': [PacoPacoMama, Javr]
        },
        # 10musume
        {
            "name": '10musume',
            "pattern": r"\d{6}.\d{2}",
            'formatter': TenMusumeFormatter,
            'webList': [TenMusume, Javr]
        },
        # one_pondo
        {
            "name": 'one_pondo',
            "pattern": r"\d{6}.\d{3}",
            'formatter': OnePondoFormatter,
            'webList': [OnePondo, Javr]
        }

    ],

    # 动漫搜刮
    'animation': [
        {
            "name": '动漫搜刮',
            'pattern': r'[a-z]{1,5}\D{1}[0-9]{1,5}|[a-z]{1,5}[0-9]{1,5}',
            'formatter': ReMediaMatterFormatter,
            'webList': [ArzonAnime]
        }
    ],

    # 欧美搜刮
    'europe': [
        {
            "name": '欧美搜刮',
            "pattern": ".+",
            'formatter': Data18Formatter,
            'webList': [Data18]
        }
    ]
}
