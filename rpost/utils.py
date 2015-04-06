# -*- coding: utf-8 -*-

from fractions import Fraction
import re
from HTMLParser import HTMLParser


def getsireid(value):
    try:
        return value[0]
    except IndexError:
        return None


def tf(values, encoding="utf-8"):
    value = ""
    for v in values:
        if v is not None and v != "":
            value = v
            break
    return value.encode(encoding).strip()


def processOR(value):
    if value == u"\u2014":
        return u'-'
    else:
        return value


def processTS(value):
    return value


def try_float(value):
    try:
        return float(value.decode('iso-8859-1').encode('utf8'))
    except ValueError:
        return 0.0
    except UnicodeEncodeError:
        return 0.0


def getfractionalodds(value):
    for v in value.split(" "):
        if '(' not in v:
            return v


def try_int(value):
    try:
        return int(value)
    except ValueError:
        return 0
    except UnicodeEncodeError:
        return 0


def toascii(value):
    return value.encode('ascii', 'ignore')


def postLBWresults(value):
    if value is None:
        return None
    elif '---' in value:
        return None
    elif value == '-':
        # winner
        return 0.0
    elif "-" in value and len(value) > 1:
        return float(Fraction(value.split('-')[0]) + Fraction(value.split('-')[1]))
    elif value == 'nse':
        return 0.02
    elif value == 'sh' or value == "shd":
        return 0.05
    elif value == 'hd':
        return 0.1
    elif value == 'nk':
        return 0.25
    elif '/' in value:
        return float(Fraction(value))
    elif value.isdigit():
        return try_float(value)
    else:
        return None


def decimalizeodds(winodds):
    """edge cases 9/4F EvensF """
    if winodds is None:
        return None
    elif "Evens" in winodds or "EvensF" in winodds:
        return 2.0
    else:
        # remove non digit chars not /
        winodds = winodds.replace("F", "").replace("J", "").replace("C", "")
        num, denom = winodds.split("/")
        dec = Fraction(int(num), int(denom)) + Fraction(1, 1)
        return round(float(dec), 2)


def processplace(place):
    if place is None:
        return None
    elif place == 'PU' or place == 'UR' or place == 'F':
        return 99
    # r_dh = r'.*[0-9].*DH$'
    else:
        return try_int(place)


# def gettotalprize(value):
# if value is None:
# return 0
#     else:
#         for p in value.split(', '):
#             newp = toascii(p)
#             ttl+= decimal.Decimal("".join(newp.split(",")))
#         return ttl
#http://www.racingpost.com/horses/result_home.sd?race_id=618500&r_date=2015-02-27&popup=yes#results_top_tabs=re_&results_bottom_tabs=ANALYSIS

# class RpostHorseItem(scrapy.Item):
#     hdob =scrapy.Field()
#     hage = scrapy.Field()
#     hsex =scrapy.Field()
#     hcolor =scrapy.Field()
#     sire =scrapy.Field()
#     rpsireid =scrapy.Field()
#     dam =scrapy.Field()
#     rpdamid=scrapy.Field()
#     damsire = scrapy.Field()
#     rpdamsireid =scrapy.Field()
#     rptrainerid = scrapy.Field()
#     owner =scrapy.Field()
#     rpownerid = scrapy.Field()
#     breeder =scrapy.Field()
#     totalsales = scrapy.Field()

def cleanUnicode(value):
    return ''.join(value.splitlines()).replace(u'\t', '').encode('ascii', 'ignore')


def getCD(value):
    # remove odd chars
    # rtn = cleanUnicode(value)
    # try:
        # rtn = rtn.split('CD')[1].split('-')[0].replace('=', '')
    return re.match(r".*\s+CD\s+=\s+([0-9.]+).*", value).group(0)
    # except:
    #     return value


def getDI(value):
    # remove odd chars
    # rtn = cleanUnicode(value)
    # try:
        # rtn = rtn.split('DI')[1].split('CD')[0].replace('=', '')
    return re.match(r".*\s+DI\s+=\s+([0-9.]+).*", value).group(0)
    # except:
    #     return value


def getraceclass(value):
    # try:
    re.match(r"(/([Class|Group][\d]+/))", value).group(1)
    # except:
    #     return value


def getracepm(value):
    # try:
    re.match(r"^.*([0-9.]+)\s[A-Za-z]+.*", value).group(0)
    # except:
    #     return value


def mystrip(value):
    return value.replace('\n\r', '')


class MLStripper(HTMLParser):

    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def fixpedcomment(value):
    value = value.encode('utf-8')
    return strip_tags(value[0]).encode('ascii', 'ignore').replace('(CLOSE)', '')
