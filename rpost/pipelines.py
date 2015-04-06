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
from scrapy.contrib.exporter import CsvItemExporter
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

                    Racename = item["racename"],
                    Racedate= item["racedate"],
                    Racecourse= item["racecourse"],
                    Racetime= item["racetime"],
                    Racepm= item.get("racepm", None),
                    Horsename= item['horsename'],
                    Racedistance = item["racedistance"],
                    Comment = item.get("comment", None),
                    Racegoing = item.get("racegoing", None),
                    Horsenumber = item.get("horsenumber", None),
                    Barrier = item.get("barrier", None),
                    RpRPR = item.get("rprpr", None),
                    RpTS = item.get("rpts", None),
                    RpOR= item.get("rpor", None),
                    Dayssincelastrun = item.get("dayssincelastrun", None),
                    Age = item["hage"],
                    WGT1 = item.get("WGT1", None),
                    WGT2 = item.get("WGT2", None),
                    WGT3 = item.get("WGT3", None),
                    WGT4 = item.get("WGT4", None),
                    WGT5 = item.get("WGT5", None),
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
                    L1raceoutcome= item.get("L1raceoutcome", None),
                    L2raceoutcome= item.get("L2raceoutcome", None),
                    L3raceoutcome= item.get("L3raceoutcome", None),
                    L4raceoutcome= item.get("L4raceoutcome", None),
                    L5raceoutcome= item.get("L5raceoutcome", None),
                    diomed =item.get("diomed", None),
                    sirecomment= item.get("sirecomment", None),
                    pedstats= item.get("pedstats", None),
                    sirename= item.get("sirename", None),
                    pedigreecomment= item.get("pedigreecomment", None),
                    DI= item.get("DI", None),
                    CD= item.get("CD", None)
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


class CsvExportPipeline(object):
    """Pipeline for exporting the scraped items to a .csv file"""

    def __init__(self):
        self.file = None
        self.exporter = None

    def open_spider(self, spider):
        self.file = open('{}.csv'.format(spider.name), 'wb')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()