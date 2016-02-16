#! /usr/bin/env python
#
# Copyright (c) 2012, Nathan Grigg, (c) 2016 Adam Morris
# All rights reserved.
# BSD License
from operator import itemgetter

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, Float
from sqlalchemy.dialects.sqlite import BLOB, VARCHAR
from .entry import Entry

# Unique per user - after this is set, DB.init_db(sqlite_url) is called.  Hardcoded for testing.
my_sqlite_url = '/Users/amorris/Library/Group Containers/5U8NS4GX82.dayoneapp2/Data/Documents/DayOne.sqlite'

class DayOneDB(object):
    def __init__(self):
        self.s = None
        self.engine = None
        self.ZENROLLMENT = None
        self.ZENTRY = None
        self.ZENTRYSYNCSTATE = None
        self.ZENTRYTOMBSTONE = None
        self.ZFEATUREENROLLMENT = None
        self.ZJOURNAL = None
        self.ZJOURNALTOMBSTONE = None
        self.ZLOCATION = None
        self.ZMUSIC = None
        self.ZPHOTO = None
        self.ZPHOTOTHUMBNAIL = None
        self.ZPROVIDER = None
        self.ZPUBLICATION = None
        self.ZPUBLISHEDENTRY = None
        self.ZREMOTEENTRY = None
        self.ZREMOTEJOURNAL = None
        self.ZSHARE = None
        self.ZSYNCGLOBALS = None
        self.ZTAG = None
        self.ZUSER = None
        self.ZUSERACTIVITY = None
        self.ZWEATHER = None
        self.ZZONEDDATE = None
        self.Z_2TAGS = None
        self.Z_METADATA = None
        # self.Z_MODELCACHE = None
        self.Z_PRIMARYKEY = None

    def init_db(self, filename):
        self.engine = create_engine('sqlite:///{0}'.format(filename))
        base = declarative_base(bind=self.engine)
        SM = sessionmaker(bind=self.engine)
        self.s = SM()

        class ZENROLLMENT(base):
            __tablename__ = 'ZENROLLMENT'
            __table_args__ = {'autoload':True}
        self.ZENROLLMENT = ZENROLLMENT

        class ZENTRY(base):
            __tablename__ = 'ZENTRY'
            Z_PK = Column(Integer, primary_key=True)
            Z_ENT = Column(Integer)
            Z_OPT = Column(Integer)
            ZSTARRED = Column(Integer)
            ZJOURNAL = Column(Integer)
            ZLOCATION = Column(Integer)
            ZMUSIC = Column(Integer)
            ZPUBLISHEDENTRY = Column(Integer)
            ZUSERACTIVITY = Column(Integer)
            ZWEATHER = Column(Integer)
            ZCREATIONDATE = Column(Float)  # timestamp as number: autoload won't work
            ZMODIFIEDDATE = Column(Float)  # timestamp as number
            ZCHANGEID = Column(VARCHAR)
            ZTEXT = Column(VARCHAR)
            ZUUID = Column(VARCHAR)
            ZCREATOR = Column(BLOB)
            ZPUBLISHURL = Column(BLOB)
            ZTIMEZONE = Column(BLOB)
        self.ZENTRY = ZENTRY

        class ZENTRYSYNCSTATE(base):
            __tablename__ = 'ZENTRYSYNCSTATE'
            __table_args__ = {'autoload':True}
        self.ZENTRYSYNCSTATE = ZENTRYSYNCSTATE

        class ZENTRYTOMBSTONE(base):
            __tablename__ = 'ZENTRYTOMBSTONE'
            __table_args__ = {'autoload':True}
        self.ZENTRYTOMBSTONE = ZENTRYTOMBSTONE

        class ZFEATUREENROLLMENT(base):
            __tablename__ = 'ZFEATUREENROLLMENT'
            __table_args__ = {'autoload':True}
        self.ZFEATUREENROLLMENT = ZFEATUREENROLLMENT

        class ZJOURNAL(base):
            __tablename__ = 'ZJOURNAL'
            __table_args__ = {'autoload':True}
        self.ZJOURNAL = ZJOURNAL

        class ZJOURNALTOMBSTONE(base):
            __tablename__ = 'ZJOURNALTOMBSTONE'
            __table_args__ = {'autoload':True}
        self.ZJOURNALTOMBSTONE = ZJOURNALTOMBSTONE

        class ZLOCATION(base):
            __tablename__ = 'ZLOCATION'
            __table_args__ = {'autoload':True}
        self.ZLOCATION = ZLOCATION

        class ZMUSIC(base):
            __tablename__ = 'ZMUSIC'
            __table_args__ = {'autoload':True}
        self.ZMUSIC = ZMUSIC

        class ZPHOTO(base):
            __tablename__ = 'ZPHOTO'
            __table_args__ = {'autoload':True}
        self.ZPHOTO = ZPHOTO

        class ZPHOTOTHUMBNAIL(base):
            __tablename__ = 'ZPHOTOTHUMBNAIL'
            __table_args__ = {'autoload':True}
        self.ZPHOTOTHUMBNAIL = ZPHOTOTHUMBNAIL

        class ZPROVIDER(base):
            __tablename__ = 'ZPROVIDER'
            __table_args__ = {'autoload':True}
        self.ZPROVIDER = ZPROVIDER

        class ZPUBLICATION(base):
            __tablename__ = 'ZPUBLICATION'
            __table_args__ = {'autoload':True}
        self.ZPUBLICATION = ZPUBLICATION

        class ZPUBLISHEDENTRY(base):
            __tablename__ = 'ZPUBLISHEDENTRY'
            __table_args__ = {'autoload':True}
        self.ZPUBLISHEDENTRY = ZPUBLISHEDENTRY

        class ZREMOTEENTRY(base):
            __tablename__ = 'ZREMOTEENTRY'
            __table_args__ = {'autoload':True}
        self.ZREMOTEENTRY = ZREMOTEENTRY

        class ZREMOTEJOURNAL(base):
            __tablename__ = 'ZREMOTEJOURNAL'
            __table_args__ = {'autoload':True}
        self.ZREMOTEJOURNAL = ZREMOTEJOURNAL

        class ZSHARE(base):
            __tablename__ = 'ZSHARE'
            __table_args__ = {'autoload':True}
        self.ZSHARE = ZSHARE

        class ZSYNCGLOBALS(base):
            __tablename__ = 'ZSYNCGLOBALS'
            __table_args__ = {'autoload':True}
        self.ZSYNCGLOBALS = ZSYNCGLOBALS

        class ZTAG(base):
            __tablename__ = 'ZTAG'
            __table_args__ = {'autoload':True}
        self.ZTAG = ZTAG

        class ZUSER(base):
            __tablename__ = 'ZUSER'
            __table_args__ = {'autoload':True}
        self.ZUSER = ZUSER

        class ZUSERACTIVITY(base):
            __tablename__ = 'ZUSERACTIVITY'
            __table_args__ = {'autoload':True}
        self.ZUSERACTIVITY = ZUSERACTIVITY

        class ZWEATHER(base):
            __tablename__ = 'ZWEATHER'
            __table_args__ = {'autoload':True}
        self.ZWEATHER = ZWEATHER

        class ZZONEDDATE(base):
            __tablename__ = 'ZZONEDDATE'
            __table_args__ = {'autoload':True}
        self.ZZONEDDATE = ZZONEDDATE

        class Z_2TAGS(base):
            __tablename__ = 'Z_2TAGS'
            __table_args__ = {'autoload':True}
        self.Z_2TAGS = Z_2TAGS

        class Z_METADATA(base):
            __tablename__ = 'Z_METADATA'
            __table_args__ = {'autoload':True}
        self.Z_METADATA = Z_METADATA

        #class Z_MODELCACHE(base):
        #    __tablename__ = 'Z_MODELCACHE'
        #    __table_args__ = {'autoload':True}
        #self.Z_MODELCACHE = Z_MODELCACHE

        class Z_PRIMARYKEY(base):
            __tablename__ = 'Z_PRIMARYKEY'
            __table_args__ = {'autoload':True}
        self.Z_PRIMARYKEY = Z_PRIMARYKEY
        base.metadata.create_all()


DB = DayOneDB()  # Singleton instance of database connection


class DBEntry(Entry):
    """
    Parse a single journal entry from the database.  Derived from plist reading Entry.

    :raises: IOError, KeyError

    Acts like a read-only dictionary.
    The keys are as defined in the plist file by the Day One App, with
    minor exceptions:

    - What Day One calls "Entry Text", we call "Text".
    - The "Location", "Weather", "Creator", and "Music" dictionaries are
      flattened, so that their subkeys are accessible as keys of the main
      dictionary.
    - The "Photo" key is added and contains the path to attached photo.
    - The "Date" key is added and contains the localized date.

    Note that the "Creation Date" contains a naive date (that is, with no
    attached time zone) corresponding to the UTC time.
    """
    def __init__(self, zuuid):
        self.data = {}
        entry = DB.s.query(DB.ZENTRY).filter(DB.ZENTRY.ZUUID == zuuid).first()

        col_map = {'Creation Date': 'ZCREATIONDATE', 'Text': 'ZTEXT', 'UUID': 'ZUUID'}

        for data_name, db_field in col_map.items():
            self.data[data_name] = getattr(entry, db_field)

        # aliases and flattening
        # self.data['Text'] = self.data.pop('Entry Text', "")
        # for key in ['Location', 'Weather', 'Music', 'Creator']:
        #     if key in self.data:
        #         new_keys = ((k, v) for k, v in self.data[key].items()
        #                     if k not in self.data) # prevent overwrite
        #         self.data.update(new_keys)


def parse_db_journal(sqlite_url):
    """Return a list of Entry objects, sorted by date"""

    DB.init_db(sqlite_url)  # Can only be called once

    journal = dict()
    rs = DB.s.query(DB.ZENTRY.ZUUID)
    for zuuid in rs:
        # zuuid is tuple with one entry (DB.ZENTRY.ZUUID,)
        entry = Entry(zuuid[0])
        journal[entry['UUID']] = entry

    if len(journal) == 0:
        raise Exception("No journal entries found in database")

    # try:
    #     photos = os.listdir(os.path.join(foldername, 'photos'))
    # except OSError:
    #     pass
    # else:
    #     for filename in photos:
    #         base = os.path.splitext(filename)[0]
    #         try:
    #             journal[base].set_photo(os.path.join('photos', filename))
    #         except KeyError:
    #             # ignore items in the photos folder with no corresponding entry
    #             pass

    # make it a list and sort
    journal = list(journal.values())
    journal.sort(key=itemgetter('Creation Date'))

    # add timezone info
    newest_tz = 'utc'
    for entry in reversed(journal):
        if "Time Zone" in entry:
            newest_tz = entry["Time Zone"]
            break

    tz = newest_tz
    for entry in reversed(journal):
        if "Time Zone" in entry:
            tz = entry["Time Zone"]
        else:
            entry.set_time_zone(tz)

        entry.set_localized_date(tz)

    return journal