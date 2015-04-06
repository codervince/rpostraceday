# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from __future__ import print_function

import logging
from Queue import Queue, Empty
from collections import defaultdict, Counter
from datetime import datetime, date
import re
import pprint

import scrapy
from scrapy.signalmanager import SignalManager
from scrapy.signals import spider_closed
from scrapy.xlib.pydispatch import dispatcher
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.contrib.pipeline.files import FilesPipeline
from scrapy.exceptions import DropItem
from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.internet.threads import deferToThreadPool
from twisted.python.threadable import isInIOThread
from twisted.python.threadpool import ThreadPool

from rpost.items import *
from rpost.models import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker, scoped_session,exc, create_session
from sqlalchemy.sql.expression import ClauseElement
from sqlalchemy.orm.exc import NoResultFound

###AGG FUNCTIONS
def getpoints(l):
    if l is None:
        return None
    pts = 0
    for r in l:
        r = str(r)
        if r == '1':
            pts+=12
        if r == '2':
            pts+=6
        if r== '3':
            pts+=4
    return pts

#extend to build raceclass for current race
def getclasschange(rname, rpm, l1class):
    if rname is None or rpm is None:
        return None
    if 'CLASS' in rname:
        try:
            cl = re.match(r".*\(CLASS\s+([\d]{1})\).*").group(1)
            l1class = re.match(r"^C([\d]{1}).*").group(1)
            return try_int(cl) - try_int(l1class)
        except:
            return None

def getledcount(l):
    try:
        for r in l:
            if r is not None:
                if u'led' in r or u'prominent' in r:
                    ct+=1
        return ct
    except:
        return 99

class RpostPipeline(object):

    def __init__(self): 
        engine = create_engine(URL(**settings.DATABASE))
        # create_tables(engine)
        create_schema(engine)
        self.Session = sessionmaker(bind=engine)
        self.cache = defaultdict(lambda: defaultdict(lambda: None))

    def process_item(self, item, spider):
        session = self.Session()

        racedays = RPRacedaydump(

                    Racename = item.get("racename", None),
                    Racedate= item.get("racedate",None),
                    Racecourse= item.get("racecourse",None),
                    Racetime= item.get("racetime",None),
                    Racepm= item.get("racepm", None),
                    Horsename= item.get('horsename', None),
                    Racedistance = item.get("racedistance",None),
                    Comment = item.get("comment", None),
                    Racegoing = item.get("racegoing", None),
                    Horsenumber = item.get("horsenumber", None),
                    Barrier = item.get("barrier", None),
                    RpRPR = item.get("rprpr", None),
                    RpTS = item.get("rpts", None),
                    RpOR= item.get("rpor", None),
                    Dayssincelastrun = item.get("dayssincelastrun", None),
                    Age = item.get("hage", None),
                    WGTL1 = item.get("WGTL1", None),
                    WGTL2 = item.get("WGTL2", None),
                    WGTL3 = item.get("WGTL3", None),
                    WGTL4 = item.get("WGTL4", None),
                    WGTL5 = item.get("WGTL5", None),
                    ClassL1 = item.get("ClassL1", None),
                    ClassL2 = item.get("ClassL2", None),
                    ClassL3 = item.get("ClassL3", None),
                    ClassL4 = item.get("ClassL4", None),
                    ClassL5 = item.get("ClassL5", None),
                    L1comment= item.get("L1comment", None),
                    L2comment= item.get("L2comment", None),
                    L3comment= item.get("L3comment", None),
                    L4comment= item.get("L4comment", None),
                    L5comment= item.get("L5comment", None),
                    L1dist= item.get("L1dist", None),
                    L2dist= item.get("L2dist", None),
                    L3dist= item.get("L3dist", None),
                    L4dist= item.get("L4dist", None),
                    L5dist= item.get("L5dist", None),
                    L1pos= item.get("L1pos", None),
                    L2pos= item.get("L2pos", None),
                    L3pos= item.get("L3pos", None),
                    L4pos= item.get("L4pos", None),
                    L5pos= item.get("L5pos", None),
                    L1ran= item.get("L1ran", None),
                    L2ran= item.get("L2ran", None),
                    L3ran= item.get("L3ran", None),
                    L4ran= item.get("L4ran", None),
                    L5ran= item.get("L5ran", None),
                    L1sp= item.get("L1sp", None),
                    L2sp= item.get("L1sp", None),
                    L3sp= item.get("L1sp", None),
                    L4sp= item.get("L1sp", None),
                    L5sp= item.get("L1sp", None),
                    L1going= item.get("L1going", None),
                    L2going= item.get("L2going", None),
                    L3going= item.get("L3going", None),
                    L4going= item.get("L4going", None),
                    L5going= item.get("L5going", None),
                    L1racecourse= item.get("L1racecourse", None),
                    L2racecourse= item.get("L1racecourse", None),
                    L3racecourse= item.get("L1racecourse", None),
                    L4racecourse= item.get("L1racecourse", None),
                    L5racecourse= item.get("L1racecourse", None),
                    diomed =item.get("diomed", None),
                    sirecomment= item.get("sirecomment", None),
                    pedstats= item.get("pedstats", None),
                    sirename= item.get("sirename", None),
                    pedigreecomment= item.get("pedigreecomment", None),
                    DI= item.get("DI", None),
                    CD= item.get("CD", None),
                    DistChangeL1 = item.get("racedistance", 0.0) - item.get("L1dist", 0.0),
                    PointsL3 = getpoints([ item.get("L1pos", None),item.get("L2pos", None),item.get("L3pos", None)]),
                    ClassChangeL1 =getclasschange(item.get("raceclass", None), item.get("racepm", None), item.get("ClassL1", None)),
                    ProminenceL3= getledcount([ item.get("L1comment", None),item.get("L2comment", None),item.get("L3comment", None) ])
                )
        try:
        # session.add(races)
            session.add(racedays)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return item

