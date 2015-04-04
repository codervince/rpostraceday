# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, Compose, Join, MapCompose, Identity
import unicodedata
import decimal
from fractions import Fraction
import re
from HTMLParser import HTMLParser

def getsireid(value):
    try:
        return value[0] 
    except:
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
        return float(value)
    except:
        return 0.0

def getfractionalodds(value):
    for v in value.split(" "):
        if '(' not in v:
            return v

def try_int(value):
    try:
        return int(value)
    except:
        return 0

def toascii(value):
    return value.encode('ascii', 'ignore')

def postLBWresults(value):
    if value is None:
        return None
    elif '---' in value:
        return None
    elif value == '-':
        #winner
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
    '''edge cases 9/4F EvensF '''
    if winodds is None:
        return None
    elif "Evens" in winodds or "EvensF" in winodds:
        return 2.0
    else:
        #remove non digit chars not /
        winodds = winodds.replace("F", "").replace("J", "").replace("C", "")
        num, denom = winodds.split("/")
        dec = Fraction(int(num), int(denom)) + Fraction(1,1)
        return round(float(dec),2)

def processplace(place):
    if place is None:
        return None
    elif place == 'PU' or place == 'UR' or place == 'F':
        return 99
# r_dh = r'.*[0-9].*DH$'
    else:
        return try_int(place)

# def gettotalprize(value):
#     if value is None:
#         return 0
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
    #remove odd chars
    # rtn = cleanUnicode(value)
    try: 
        # rtn = rtn.split('CD')[1].split('-')[0].replace('=', '')
        return re.match(r".*\s+CD\s+=\s+([0-9.]+).*", value).group(0)
    except:
        return value

def getDI(value):
    #remove odd chars
    # rtn = cleanUnicode(value)
    try: 
        # rtn = rtn.split('DI')[1].split('CD')[0].replace('=', '')
        return re.match(r".*\s+DI\s+=\s+([0-9.]+).*", value).group(0)
    except:
        return value

def getraceclass(value):
    try:
        re.match(r"(/([Class|Group][\d]+/))", value).group(1)
    except:
        return value

def getracepm(value):
    try:
       re.match(r"^.*([0-9.]+)\s[A-Za-z]+.*", value).group(0)
    except:
        return value

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
    return strip_tags(value[0]).encode('ascii', 'ignore').replace('(CLOSE)', '')


class HorseItem(scrapy.Item):
    racecourse = scrapy.Field()
    racetime = scrapy.Field()
    racename  =scrapy.Field()
    raceclass = scrapy.Field()
    racepm =scrapy.Field()
    racedate =scrapy.Field()
    racedistance =scrapy.Field()
    racegoing =scrapy.Field()
    horsenumber =scrapy.Field()
    horsename =scrapy.Field()
    comment =scrapy.Field()
    todaysWgt_dec=scrapy.Field()
    todaysWgt=scrapy.Field()
    barrier=scrapy.Field()
    dayssincelastrun=scrapy.Field()
    rpRPR=scrapy.Field()
    rpOR=scrapy.Field()
    rpTS=scrapy.Field()
    timestamp =scrapy.Field()
    bestodds =scrapy.Field()
    hage =scrapy.Field()
    WGT1 =scrapy.Field()
    WGT2 =scrapy.Field()
    WGT3 =scrapy.Field()
    WGT4 =scrapy.Field()
    WGT5 =scrapy.Field()
    ClassL1 = scrapy.Field()
    ClassL2 = scrapy.Field()
    ClassL3 = scrapy.Field()
    ClassL4 = scrapy.Field()
    ClassL5 = scrapy.Field()
    L1comment = scrapy.Field()
    L2comment = scrapy.Field()
    L3comment = scrapy.Field()
    L4comment = scrapy.Field()
    L5comment = scrapy.Field()
    L1raceoutcome = scrapy.Field()
    L2raceoutcome = scrapy.Field()
    L3raceoutcome = scrapy.Field()
    L4raceoutcome = scrapy.Field()
    L5raceoutcome = scrapy.Field()
    diomed = scrapy.Field()
    sirecomment = scrapy.Field()
    pedstats = scrapy.Field()
    sirename = scrapy.Field()
    pedigreecomment = scrapy.Field()
    DI = scrapy.Field()
    CD = scrapy.Field()
    Family = scrapy.Field()
    Pedprizemoney = scrapy.Field()
    L1pos = scrapy.Field()
    L2pos = scrapy.Field()
    L3pos = scrapy.Field()
    L4pos = scrapy.Field()
    L5pos = scrapy.Field()

class RacedayItemLoader(ItemLoader):
     default_item_class = HorseItem
     # default_output_processor = Compose(TakeFirst(), mystrip)
     # ClassL1_out = TakeFirst()
     # ClassL2_out = TakeFirst()
     # ClassL3_out = TakeFirst()
     # ClassL4_out = TakeFirst()
     # ClassL5_out = TakeFirst()
     # L1comment_out = TakeFirst()
     # L2comment_out = TakeFirst()
     # L3comment_out = TakeFirst()
     # L4comment_out = TakeFirst()
     # L5comment_out = TakeFirst()
     # racedistance_out = TakeFirst()
     # raceclass_out = Join()
     # racename_out = Join()
     # racetime_out = TakeFirst()
     # timestamp_out = TakeFirst()
     # sirecomment_out = TakeFirst()
     # racegoing_out = TakeFirst()
     # age_out = TakeFirst()
     barrier_out  = Compose(TakeFirst(), try_int)
     horsenumber_out  = Compose(TakeFirst(), try_int)
     dayssincelastrun_out  = Compose(TakeFirst(), try_int)
     # comment_out = TakeFirst()

     # pedstats_out  = TakeFirst()
     # horsename_out  = TakeFirst()
     # L1raceoutcome= TakeFirst()
     # L2raceoutcome= TakeFirst()
     # L3raceoutcome= TakeFirst()
     # L4raceoutcome= TakeFirst()
     # L5raceoutcome= TakeFirst()
     # WGT1= TakeFirst()
     # WGT2= TakeFirst()
     # WGT3= TakeFirst()
     # WGT4= TakeFirst()
     # WGT5= TakeFirst()
     # # default_output_processor = Compose(TakeFirst(), unicode, unicode.strip)
     # DI_out = Compose(TakeFirst(), unicode, unicode.strip)
     CD_out = Compose(TakeFirst(), unicode, unicode.strip)
     # pedstats_out =Compose(Join(),unicode, unicode.strip, cleanUnicode)
     racename_out =Compose(Join(),unicode, unicode.strip)
     # pedigreecomment_out =Compose(TakeFirst(), fixpedcomment)
     # pedstats_out = Compose(Join(),unicode, unicode.strip)
     # diomed_out =Join()
     rpOR_out=Compose(TakeFirst(), try_int)
     rpRPR_out=Compose(TakeFirst(),try_int)
     RPTS_out =Compose(TakeFirst(),try_int)
     # comment_out = TakeFirst()
     # racecourse_out = Compose(TakeFirst(), unicode, unicode.strip)

     # sirename_out = Compose(TakeFirst(), unicode, unicode.strip)
     # racedate_out = Compose(TakeFirst(), unicode, unicode.strip)
     # racetime_out = Compose(TakeFirst(), unicode, unicode.strip)
     # racecourse_out = Compose(TakeFirst(), unicode, unicode.strip)
     # sirecomment_out = Compose(TakeFirst(), unicode, unicode.strip)
     # racedistance_out = Compose(TakeFirst(), unicode, unicode.strip)
     # raceclass_out = Compose(Join(), unicode, unicode.strip)
     # racepm_out = Compose(TakeFirst(), unicode, unicode.strip, getracepm)
     # L1raceoutcome = Compose(TakeFirst(), unicode, unicode.strip)
     # L2raceoutcome = Compose(TakeFirst(), unicode, unicode.strip)
     # L3raceoutcome = Compose(TakeFirst(), unicode, unicode.strip) 
     # L4raceoutcome = Compose(TakeFirst(), unicode, unicode.strip)
     # L5raceoutcome = Compose(TakeFirst(), unicode, unicode.strip)

