# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

##TODO: Fix L1dist at present returns 2nd char of going!
## place should return PU F etc
## L1sp etc does not return correct value ALL same
## also racecourse returns 1st as ALL values..
## Prominency class change does not work


import scrapy
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, Compose, Join, MapCompose, Identity
import unicodedata
import decimal
from fractions import Fraction
import re
from HTMLParser import HTMLParser

def isFavorite(winodds):
    if winodds is None:
        return None
    return "F" or "J" or "C" in winodds

def decimalizeodds(winodds):
    '''edge cases 9/4F EvensF '''
    if winodds is None:
        return None
    elif u'Evens' in winodds or u'EvensF' in winodds:
        return 2.0
    else:
        #remove non digit chars not /
        try:
            winodds = winodds.replace(u'F', u'').replace(u'f', u'').replace(u'J', u'').replace(u'C', u'')
            num, denom = winodds.split(u'/')
            return try_float( (try_int(num)/int(denom)) + 1.0 )
        except:
            return None


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

# def decimalizeodds(winodds):
#     '''edge cases 9/4F EvensF '''
#     if winodds is None:
#         return None
#     elif "Evens" in winodds or "EvensF" in winodds:
#         return 2.0
#     else:
#         #remove non digit chars not /
#         winodds = winodds.replace("F", "").replace("J", "").replace("C", "")
#         num, denom = winodds.split("/")
#         dec = Fraction(int(num), int(denom)) + Fraction(1,1)
#         return round(float(dec),2)

def processplace(place):
    if place is None:
        return None
    elif place == 'PU' or place == 'UR' or place == 'F':
        return 99
# r_dh = r'.*[0-9].*DH$'
    else:
        return try_int(place)

def disttofurlongs(x):
    '''ex 2m2f50y'''
    miles = 0
    furlongs = 0
    yards = 0
    if u'm' in x:
        miles= try_float(re.match(r".*([\d]{1})m.*",x).group(1))
    if 'y' in x:
        yards= try_int(re.match(r".*([\d]{1,3})y.*",x).group(1))
        #yards in furlongs
        yards = try_float(yards/110)
    if 'f' in x:
        furlongs= try_float(re.match(r".*([\d]{1})f.*",x).group(1))
    return miles*8 + furlongs*1 + yards*0.0045454

def processplace(place):
    if place is None:
        return None
    elif place == 'PU' or place == 'UR' or place == 'F':
        return 99
# r_dh = r'.*[0-9].*DH$'
    else:
        return try_int(place)
    # if u'f' in x and (u'm' not in x and u'y' not in x):
    #     return try_int(x.replace('f', ''))
    # if (u'f' in x and u'm' in x) and (u'y' not in x):
    #     miles, furlongs = try_int(x.split(u'm')[0]), try_int(x.split(u'f')[0].split(u'm')[1])
    # # if u'f' in x and u'm' not in x:
    # #     furlongs = try_int(x.split("f")[0])
    # if ('f' in x and 'y' in x) and ('m' not in x):
    #     furlongs, yards = try_int(x.split(u'f')[0]), try_int(x.split(u'f')[0].split( u'y')[1])
    # if (u'm' in x and u'y' in x) and (u'f' not in x):
    #     miles, yards = try_int(x.split(u'm')[0]), try_int(x.split(u'm')[0].split( u'y')[1])
    # return miles*8 + furlongs
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

def getabbracegoing(x):
    if x is None:
        return None
    d= {'Good To Soft':'GS','Soft':'Sft', 'Heavy':'Hy', 'Standard':'Std','Good':'Gd', 'Firm': 'Fm', 'Very Soft': 'VS'}
    temp = d.get(str(x))
    if temp:
        return temp
    else:
        return x


def cleanUnicode(value):
    return ''.join(value.splitlines()).replace(u'\2014', '').encode('ascii', 'ignore')



# def getDI(value):
#     #remove odd chars
#     # rtn = cleanUnicode(value)
#     try: 
#         # rtn = rtn.split('DI')[1].split('CD')[0].replace('=', '')
#         return re.match(r".*\s+DI\s+=\s+([0-9.]+).*", value).group(0)
#     except:
#         return value

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

def mystrip(value):
    return value.replace(u'\n', u'').replace(u'\u2014', u'-').replace(u'\t', u'').replace(u'\r', u'').replace(u'\xa0', u'')

###INPUT PROCESSORS 


def strip_dashes(x):
    return x.strip('-')


def gettodayspm(x):
    try:
        x= re.match('GBP([0-9,]+).*', x.replace(u'\xa3', 'GBP')).group(1)
        return str(int(x.replace(',', ''))/1000) + u'K'
        # return re.match(r".*([0-9/.]+).*", x).group(1)
    except:
        return x

def getpm(x):
    try:
        return x.split(u' ')[1]
    except:
        return u'No PM'

def getcd(x):
    try: 
        # rtn = rtn.split('CD')[1].split('-')[0].replace('=', '')
        return re.match(r".*CD\s=\s([0-9.]{3,4}).*", x).group(1)
    except:
        return u'N/A'

def getdi(x):
    try: 
        # rtn = rtn.split('DI')[1].split('CD')[0].replace('=', '')
        return re.match(r".*DI\s=\s([0-9.]{3,4}).*", x).group(1)
    except:
        return u'N/A'

def removevulgarfracts(x):
    return x.replace(u'\xbcL', u'0.25L').replace(u'\xbdL', u'0.5L').replace(u'\xbeL', u'0.75L')

def getnocomment(x):
    if u'Click to view result' in x:
        return 'No Comment'
    else:
        return x



def getgoing(x):
    try:
        y = re.match(r".*\d{1,2}(\w{2,3}).*", x).group(1)
    except:
        return x

def getracecourse(x):
    try:
        return re.match(r"[^0-9](\w{3}).*", x).group(1)
    except:
        return x

#what about PU F etc?
def getLpos(x):
    #raceoutcome
    try:
        return try_int(re.match(r".*(\d+)\/\d{1,2}\s+\(.*", x.replace(u'\n',u'')).group(1))
    except:
        return None

def getLran(x):
    #raceoutcome
    try:
        return try_int(re.match(r".*\/(\d+)\s+\(.*", x.replace(u'\n',u'')).group(1))
    except:
        return None

def getLdist(x):
    try:
        return try_float(re.match(r".*([0-9.]{1,4})[A-Z]{1}.*",x.replace(u'\n',u'')).group(1))
    except:
        return x

def getLracecourse(x):
    try:
        return re.match(r".*(\d+)",x.replace(u'\n',u'')).group(1)
    except:
        return x

def getLgoing(x):
    try:
        return re.match(r".*\d(\w{1,2})",x.replace(u'\n',u'')).group(1)
    except:
        return x

def getLsp(x):
    try:
        return decimalizeodds(re.match(r".*(\d{1,2}\/\d{1,2}F{0,1}).*", x.replace(u'\n',u'')).group(1))
    except:
        return x

def getLlbw(x):
    try:
        return re.findall(r".*\((.*)L\s.*", x)
    except:
        return x

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
    WGTL1 =scrapy.Field()
    WGTL2 =scrapy.Field()
    WGTL3 =scrapy.Field()
    WGTL4 =scrapy.Field()
    WGTL5 =scrapy.Field()
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
    L1ran = scrapy.Field()
    L2ran = scrapy.Field()
    L3ran = scrapy.Field()
    L4ran = scrapy.Field()
    L5ran = scrapy.Field()
    L1dist = scrapy.Field()
    L2dist = scrapy.Field()
    L3dist = scrapy.Field()
    L4dist = scrapy.Field()
    L5dist = scrapy.Field()
    L1racecourse = scrapy.Field()
    L2racecourse = scrapy.Field()
    L3racecourse = scrapy.Field()
    L4racecourse = scrapy.Field()
    L5racecourse = scrapy.Field()
    L1going = scrapy.Field()
    L2going = scrapy.Field()
    L3going = scrapy.Field()
    L4going = scrapy.Field()
    L5going = scrapy.Field()
    L1sp = scrapy.Field()
    L2sp = scrapy.Field()
    L3sp = scrapy.Field()
    L4sp = scrapy.Field()
    L5sp = scrapy.Field()
    pmL1 = scrapy.Field()
    pmL2 = scrapy.Field()
    pmL3 = scrapy.Field()
    pmL4 = scrapy.Field()
    pmL5 = scrapy.Field()
    L1lbw = scrapy.Field()
    L2lbw = scrapy.Field()
    L3lbw = scrapy.Field()
    L4lbw = scrapy.Field()
    L5lbw = scrapy.Field()
    record_1 = scrapy.Field()
    record_1_stats = scrapy.Field()
    record_2 = scrapy.Field()
    record_2_stats = scrapy.Field()
    record_3 = scrapy.Field()
    record_3_stats = scrapy.Field()
    record_4 = scrapy.Field()
    record_4_stats = scrapy.Field()
    record_5 = scrapy.Field()
    record_5_stats = scrapy.Field()

class RacedayItemLoader(ItemLoader):
     default_item_class = HorseItem
     # default_input_processor = MapCompose(unicode, unicode.strip)
     # default_output_processor = TakeFirst()
     pmL1_in = MapCompose(getpm)
     pmL2_in = MapCompose(getpm)
     pmL3_in = MapCompose(getpm)
     pmL4_in = MapCompose(getpm)
     pmL5_in = MapCompose(getpm)
     pmL1_out = TakeFirst()
     pmL2_out = TakeFirst()
     pmL3_out = TakeFirst()
     pmL4_out = TakeFirst()
     pmL5_out = TakeFirst()
     ClassL1_out = TakeFirst()
     ClassL2_out = TakeFirst()
     ClassL3_out = TakeFirst()
     ClassL4_out = TakeFirst()
     ClassL5_out = TakeFirst()
     L1comment_in = MapCompose(getnocomment)
     L1comment_out = TakeFirst()
     L2comment_out = TakeFirst()
     L3comment_out = TakeFirst()
     L4comment_out = TakeFirst()
     L5comment_out = TakeFirst()

     diomed_in = MapCompose(unicode.strip,mystrip)
     diomed_out = Compose(Join())
     
     # raceclass_in = MapCompose(Join())
     raceclass_in = Compose(Join(), mystrip)
     raceclass_out = TakeFirst()
     racename_in = Compose(Join(), mystrip)
     racename_out = TakeFirst()


     racepm_in = MapCompose(gettodayspm)
     racepm_out = TakeFirst()

     racecourse_in = MapCompose(unicode.strip)
     racecourse_out = Compose(Join(), unicode.strip)
     horsename_out = TakeFirst()

     barrier_out = TakeFirst()
     dayssincelastrun_out = TakeFirst()



     pedigreecomment_in = MapCompose(strip_tags)
     pedigreecomment_out =Compose(TakeFirst(),unicode.strip, mystrip)
     # CD_in = Join()
     # CD_out = Compose(mystrip, getCD)
     # DI_in = MapCompose(getDI)
     L1raceoutcome_in = MapCompose(removevulgarfracts, unicode.strip,mystrip)
     L1raceoutcome_out = TakeFirst()
     L2raceoutcome_in = MapCompose(removevulgarfracts,unicode.strip,mystrip)
     L2raceoutcome_out = TakeFirst()
     L3raceoutcome_in = MapCompose(removevulgarfracts,unicode.strip,mystrip)
     L3raceoutcome_out = TakeFirst()
     L4raceoutcome_in = MapCompose(removevulgarfracts,unicode.strip,mystrip)
     L4raceoutcome_out = TakeFirst()
     L5raceoutcome_in = MapCompose(removevulgarfracts,unicode.strip,mystrip)
     L5raceoutcome_out = TakeFirst()
     racename_out = Compose(Join())

     L1dist_in = MapCompose(unicode.strip)
     L1dist_out = Compose(TakeFirst(), getLdist)
     L1pos_in = MapCompose(unicode.strip,getLpos)
     L1pos_out = TakeFirst()
     L1ran_in = MapCompose(unicode.strip,getLran)
     L1ran_out = TakeFirst()
     L1racecourse_in = MapCompose(unicode.strip,getLracecourse)
     L1racecourse_out = TakeFirst()
     L1going_in = MapCompose(unicode.strip,getLgoing)
     L1going_out = TakeFirst()
     L1sp_in = MapCompose(unicode.strip)
     L1sp_out = Compose(TakeFirst(), getLsp)
     
     L2dist_in = MapCompose(unicode.strip)
     L2dist_out = Compose(TakeFirst(), getLdist)
     L2pos_in = MapCompose(unicode.strip,getLpos)
     L2pos_out = TakeFirst()
     L2ran_in = MapCompose(unicode.strip,getLran)
     L2ran_out = TakeFirst()
     L2racecourse_in = MapCompose(unicode.strip,getLracecourse)
     L2racecourse_out = TakeFirst()
     L2going_in = MapCompose(unicode.strip,getLgoing)
     L2going_out = TakeFirst()
     L2sp_in = MapCompose(unicode.strip)
     L2sp_out = Compose(TakeFirst(), getLsp)


     L3dist_in = MapCompose(unicode.strip)
     L3dist_out = Compose(TakeFirst(), getLdist)
     L3pos_in = MapCompose(unicode.strip,getLpos)
     L3pos_out = TakeFirst()
     L3ran_in = MapCompose(unicode.strip,getLran)
     L3ran_out = TakeFirst()
     L3racecourse_in = MapCompose(unicode.strip,getLracecourse)
     L3racecourse_out = TakeFirst()
     L3going_in = MapCompose(unicode.strip,getLgoing)
     L3going_out = TakeFirst()
     L3sp_in = MapCompose(unicode.strip)
     L3sp_out = Compose(TakeFirst(), getLsp)

     L4dist_in = MapCompose(unicode.strip)
     L4dist_out = Compose(TakeFirst(), getLdist)
     L4pos_in = MapCompose(unicode.strip,getLpos)
     L4pos_out = TakeFirst()
     L4ran_in = MapCompose(unicode.strip,getLran)
     L4ran_out = TakeFirst()
     L4racecourse_in = MapCompose(unicode.strip,getLracecourse)
     L4racecourse_out = TakeFirst()
     L4going_in = MapCompose(unicode.strip,getLgoing)
     L4going_out = TakeFirst()
     L4sp_in = MapCompose(unicode.strip)
     L4sp_out = Compose(TakeFirst(), getLsp)

     L5dist_in = MapCompose(unicode.strip)
     L5dist_out = Compose(TakeFirst(), getLdist)
     L5pos_in = MapCompose(unicode.strip,getLpos)
     L5pos_out = TakeFirst()
     L5ran_in = MapCompose(unicode.strip,getLran)
     L5ran_out = TakeFirst()
     L5racecourse_in = MapCompose(unicode.strip,getLracecourse)
     L5racecourse_out = TakeFirst()
     L5going_in = MapCompose(unicode.strip,getLgoing)
     L5going_out = TakeFirst()
     L5sp_in = MapCompose(unicode.strip)
     L5sp_out = Compose(TakeFirst(), getLsp)

     L1lbw_in = MapCompose(unicode.strip,getLlbw)
     L1lbw_out = TakeFirst()
     L2lbw_in = MapCompose(unicode.strip,getLlbw)
     L2lbw_out = TakeFirst()
     L3lbw_in = MapCompose(unicode.strip,getLlbw)
     L3lbw_out = TakeFirst()
     L4lbw_in = MapCompose(unicode.strip,getLlbw)
     L4lbw_out = TakeFirst()
     L5lbw_in = MapCompose(unicode.strip,getLlbw)
     L5lbw_out = TakeFirst()
     # L2lbw_in

     # # L5raceoutcome= TakeFirst()
     WGTL1_in = MapCompose(unicode.strip)
     WGTL2_in = MapCompose(unicode.strip)
     WGTL3_in = MapCompose(unicode.strip)
     WGTL4_in = MapCompose(unicode.strip)
     WGTL5_in = MapCompose(unicode.strip)
     WGTL1_out= TakeFirst()
     WGTL2_out= TakeFirst()
     WGTL3_out= TakeFirst()
     WGTL4_out= TakeFirst()
     WGTL5_out= TakeFirst()

     comment_in = MapCompose(unicode.strip, mystrip)
     comment_out = TakeFirst()
     
     racetime_out = TakeFirst()

     racedistance_in = MapCompose(unicode.strip,disttofurlongs)
     racedistance_out = TakeFirst()

     racedate_out= TakeFirst()
     
     ##INT
     racegoing_in = MapCompose(unicode.strip)
     racegoing_out = Compose(TakeFirst(),getabbracegoing)
     rpRPR_out = Compose(TakeFirst(),try_int)
     rpTS_out = Compose(TakeFirst(),try_int)
     rpOR_out = Compose(TakeFirst(),try_int)
     barrier_out = Compose(TakeFirst(),try_int)
     hage_out = Compose(TakeFirst(),try_int)
     dayssincelastrun_out = Compose(TakeFirst(),try_int)
     horsenumber_out = Compose(TakeFirst(),try_int)

     sirecomment_out = TakeFirst()
     timestamp_out = TakeFirst()

     pedstats_in = Join()
     pedstats_out = Compose(TakeFirst(),unicode.strip, mystrip)

     CD_in = Join()
     CD_out = Compose(TakeFirst(),unicode.strip, mystrip, getcd)

     DI_in = Join()
     DI_out = Compose(TakeFirst(),unicode.strip, mystrip, getdi)

     record_1_in = MapCompose(unicode.strip, mystrip)
     record_1_stats_in = MapCompose(unicode.strip, mystrip)
     record_1_out = TakeFirst()
     record_1_stats_out = TakeFirst()
     record_2_in = MapCompose(unicode.strip, mystrip)
     record_2_stats_in = MapCompose(unicode.strip, mystrip)
     record_2_out = TakeFirst()
     record_2_stats_out = TakeFirst()
     record_3_in = MapCompose(unicode.strip, mystrip)
     record_3_stats_in = MapCompose(unicode.strip, mystrip)
     record_3_out = TakeFirst()
     record_3_stats_out = TakeFirst()
     record_4_in = MapCompose(unicode.strip, mystrip)
     record_4_stats_in = MapCompose(unicode.strip, mystrip)
     record_4_out = TakeFirst()
     record_4_stats_out = TakeFirst()
     record_5_in = MapCompose(unicode.strip, mystrip)
     record_5_stats_in = MapCompose(unicode.strip, mystrip)
     record_5_out = TakeFirst()
     record_5_stats_out = TakeFirst()
     # # # default_output_processor = Compose(TakeFirst(), unicode, unicode.strip)
     # # DI_out = Compose(TakeFirst(), unicode, unicode.strip)
     # CD_out = Compose(TakeFirst(), unicode, unicode.strip)
     # # pedstats_out =Compose(Join(),unicode, unicode.strip, cleanUnicode)
     # racename_out =Compose(Join(),unicode, unicode.strip)
     # # pedigreecomment_out =Compose(TakeFirst(), fixpedcomment)
     # # pedstats_out = Compose(Join(),unicode, unicode.strip)
     # # diomed_out =Join()
     # rpOR_out=Compose(TakeFirst(), try_int)
     # rpRPR_out=Compose(TakeFirst(),try_int)
     # RPTS_out =Compose(TakeFirst(),try_int)
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

