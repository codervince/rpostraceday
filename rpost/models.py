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
    RpRPR = Column("rprpr", String(255))
    RpTS = Column("rpts", String(255))
    RpOR = Column("rpor", String(255))
    Racegoing= Column("racegoing", String(255))
    Dayssincelastrun = Column("dayssincelastrun", Integer)
    Age = Column("age", String(255))
    WGT1 = Column("wgt1", String(255))
    WGT2 = Column("wgt2", String(255))
    WGT3 = Column("wgt3", String(255))
    WGT4 = Column("wgt4", String(255))
    WGT5 = Column("wgt5", String(255))
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
    L1raceoutcome = Column("l1raceoutcome", String(255))
    L2raceoutcome = Column("l2raceoutcome", String(255))
    L3raceoutcome = Column("l3raceoutcome", String(255))
    L4raceoutcome = Column("l4raceoutcome", String(255))
    L5raceoutcome = Column("l5raceoutcome", String(255))
    diomed = Column("diomed", Text)
    sirecomment = Column("sirecomment", Text)    
    pedstats = Column("pedstats", Text)
    sirename = Column("sirename", String(255))
    pedigreecomment = Column("pedigreecomment", Text)
    DI = Column("di", String(255))
    CD = Column("cd", String(255))

def get_engine():
    return create_engine(URL(**settings.DATABASE), pool_size=0)
    # return DBDefer(URL(**settings.DATABASE))

def create_schema(engine):
    ModelBase.metadata.create_all(engine)

