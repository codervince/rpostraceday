#OUTSOURCE THIS TO racespg.py

# -*- coding: utf-8 -*-
#/Users/vmac/RACING1/HKG/scrapers/dist/hkjc
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, UniqueConstraint, CheckConstraint, Time, Float, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import BYTEA, TIMESTAMP
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import relationship, backref
from sqlalchemy.pool import SingletonThreadPool
#for Oracle, Firebird
from sqlalchemy import *
import settings


#for multithreading
# from twisted.web import xmlrpc, server
# from twisted.internet import reactor
Base = declarative_base()
engine = create_engine(URL(**settings.DATABASE))
metadata = MetaData(bind=engine)

ModelBase = declarative_base()

    # racecourse = scrapy.Field()
    # racetime = scrapy.Field()
    # racename  =scrapy.Field()
    # raceclass = scrapy.Field()
    # racepm  =scrapy.Field()
    # racedate =scrapy.Field()
    # racedistance =scrapy.Field()
    # horsename =scrapy.Field()
    # comment =scrapy.Field()
    # timestamp =scrapy.Field()
    # bestodds =scrapy.Field()
    # hage =scrapy.Field()
    # WGT1 =scrapy.Field()
    # WGT2 =scrapy.Field()
    # WGT3 =scrapy.Field()
    # WGT4 =scrapy.Field()
    # WGT5 =scrapy.Field()
    # ClassL1 = scrapy.Field()
    # ClassL2 = scrapy.Field()
    # ClassL3 = scrapy.Field()
    # ClassL4 = scrapy.Field()
    # ClassL5 = scrapy.Field()
    # L1comment = scrapy.Field()
    # L2comment = scrapy.Field()
    # L3comment = scrapy.Field()
    # L4comment = scrapy.Field()
    # L5comment = scrapy.Field()
    # L1raceoutcome = scrapy.Field()
    # L2raceoutcome = scrapy.Field()
    # L3raceoutcome = scrapy.Field()
    # L4raceoutcome = scrapy.Field()
    # L5raceoutcome = scrapy.Field()
    # diomed = scrapy.Field()
    # sirecomment = scrapy.Field()
    # pedstats = scrapy.Field()
    # sirename = scrapy.Field()
    # pedigreecomment = scrapy.Field()
    # DI = scrapy.Field()
    # CD = scrapy.Field()

class RPRacedaydump(ModelBase):
    __tablename__ = "gbracedaydump"
    id = Column(Integer, primary_key=True)
    Racecourse = Column("racecourse", String(255))
    Racetime = Column("racetime", String(255))
    Racename = Column("racename", String(255))
    Raceclass = Column("raceclass", String(255))
    Racedate = Column("racedate", String(255))
    Racepm = Column("racepm", String(255))
    Racedistance = Column("racedistance", String(255))
    Horsename = Column("horsename", String(255))
    Comment = Column("comment", Text)
    Horsenumber = Column("horsenumber", Integer)
    Barrier = Column("barrier", Integer)
    RpRPR = Column("rprpr", Integer)
    RpTS = Column("rpts", Integer)
    RpOR = Column("rpor", Integer)
    Racegoing= Column("racegoing", String(255))
    Dayssincelastrun = Column("dayssincelastrun", Integer)
    Age = Column("age", String(255))
    WGTL1 = Column("wgtl1", String(255))
    WGTL2 = Column("wgtl2", String(255))
    WGTL3 = Column("wgtl3", String(255))
    WGTL4 = Column("wgtl4", String(255))
    WGTL5 = Column("wgtl5", String(255))
    ClassL1 = Column("class1", String(255))
    ClassL2 = Column("class2", String(255))
    ClassL3 = Column("class3", String(255))
    ClassL4 = Column("class4", String(255))
    ClassL5 = Column("class5", String(255))
    L1comment = Column("l1comment", String(255))
    L2comment = Column("l2comment", String(255))
    L3comment = Column("l3comment", String(255))
    L4comment = Column("l4comment", String(255))
    L5comment = Column("l5comment", String(255))
    L1ran = Column("l1ran", Integer)
    L2ran = Column("l2ran", Integer)
    L3ran = Column("l3ran", Integer)
    L4ran = Column("l4ran", Integer)
    L5ran = Column("l5ran", Integer)
    L1pos = Column("l1pos", String(255))
    L2pos = Column("l2pos", String(255))
    L3pos = Column("l3pos", String(255))
    L4pos = Column("l4pos", String(255))
    L5pos = Column("l5pos", String(255))

    L1lbw = Column("l1lbw", String(255))
    L2lbw = Column("l2lbw", String(255))
    L3lbw = Column("l3lbw", String(255))
    L4lbw = Column("l4lbw", String(255))
    L5lbw = Column("l5lbw", String(255))

    record_1 = Column("record1", String(255))
    record_1_stats = Column("record1stats", String(255))
    record_2 = Column("record2", String(255))
    record_2_stats = Column("record2stats", String(255))  
    record_3 = Column("record3", String(255))
    record_3_stats = Column("record3stats", String(255))  
    record_4 = Column("record4", String(255))
    record_4_stats = Column("record4stats", String(255))  
    record_5 = Column("record5", String(255))
    record_5_stats = Column("record5stats", String(255))  
    #ADD NUMPOS
    L1sp = Column("l1sp", Float)
    L2sp = Column("l2sp", Float)
    L3sp = Column("l3sp", Float)
    L4sp = Column("l4sp", Float)
    L5sp = Column("l5sp", Float)
    L1dist = Column("l1dist", Float)
    L2dist = Column("l2dist", Float)
    L3dist = Column("l3dist", Float)
    L4dist = Column("l4dist", Float)
    L5dist = Column("l5dist", Float)
    L1going = Column("l1going", String(255))
    L2going = Column("l2going", String(255))
    L3going = Column("l3going", String(255))
    L4going = Column("l4going", String(255))
    L5going = Column("l5going", String(255))
    L1racecourse =Column("L1racecourse", String(255))
    L2racecourse =Column("L2racecourse", String(255))
    L3racecourse =Column("L3racecourse", String(255))
    L4racecourse =Column("L4racecourse", String(255))
    L5racecourse =Column("L5racecourse", String(255))
    # L1raceoutcome = Column("l1raceoutcome", String(255))
    # L2raceoutcome = Column("l2raceoutcome", String(255))
    # L3raceoutcome = Column("l3raceoutcome", String(255))
    # L4raceoutcome = Column("l4raceoutcome", String(255))
    # L5raceoutcome = Column("l5raceoutcome", String(255))
    diomed = Column("diomed", Text)
    sirecomment = Column("sirecomment", Text)    
    pedstats = Column("pedstats", Text)
    sirename = Column("sirename", String(255))
    pedigreecomment = Column("pedigreecomment", Text)
    DI = Column("di", String(255))
    CD = Column("cd", String(255))
    DistChangeL1 =Column("distchangel1", Float)
    PointsL3 = Column("pointsl3", Integer)
    ClassChangeL1 = Column("classchangel1", Integer)
    ProminenceL3 = Column("prominencel3", Integer)

def get_engine():
    return create_engine(URL(**settings.DATABASE), pool_size=0)
    # return DBDefer(URL(**settings.DATABASE))

def create_schema(engine):
    ModelBase.metadata.create_all(engine)

