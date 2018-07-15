import sqlite3 as lite
import os
import logging
import numpy as np

class Smoother(object):
    def __init__(self, win_size, threshold):

        self.buffer = np.zeros(win_size)
        self.current_val = 0.0
        self.threshold = threshold

    def put(self, sample):
        """
            Add a sample to the smoother, return True if the smoothed data changed
        """
        # shift data
        self.buffer[:-1] = self.buffer[1:]
        self.buffer[-1] = sample

        avg = np.mean(self.buffer)

        if np.abs(avg-self.current_val) > self.threshold:
            self.current_val = avg
            return True

        return False

    def get(self):
        return self.current_val



class Radio(object):
    FIELDS = ["id", "name", "uri", "position"]
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return "Radio <{}, {}, {}, {}>".format(self.id, self.name, self.uri, self.position)


class RssFeed(object):
    FIELDS = ["id", "name", "uri", "position"]
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return "RSS Feed <{}, {}, {}, {}>".format(self.id, self.name, self.uri, self.position)

class RedBoxDataBase(object):
    def __init__(self, filename):
        self.logger = logging.getLogger(__name__)


        db_exists = os.path.isfile(filename)

        try:
            self.conn = lite.connect(filename)
        except Exception as e:
            self.logger.error("Can't open db file {}: {}".format(filename, str(e)))

        if not db_exists:
            self.initDb()


    def initDb(self):
        self.logger.info("DB doesn't exist, creating")
        c = self.conn.cursor()
        c.execute("CREATE TABLE radios ( id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, name	TEXT, uri	TEXT,  position	REAL  );")
        self.conn.commit()

        c = self.conn.cursor()
        c.execute("CREATE TABLE rss ( id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, name	TEXT, uri	TEXT,  position	REAL  );")
        self.conn.commit()


    def getRadios(self):
        radios = []
        c = self.conn.cursor()
        for row in c.execute("SELECT {} FROM radios ORDER BY position".format(", ".join(Radio.FIELDS))):
            radio = {}
            for i in range(len(Radio.FIELDS)):
                radio[Radio.FIELDS[i]] = row[i]
            radios.append(Radio(**radio))

        return radios

    def getRadiosKeywordPosition(self):
        radios = {}
        c = self.conn.cursor()
        for row in c.execute("SELECT {} FROM radios".format(", ".join(Radio.FIELDS))):
            radio = {}
            for i in range(len(Radio.FIELDS)):
                radio[Radio.FIELDS[i]] = row[i]
            radios[radio["position"]] = Radio(**radio)

        return radios

    def getRadio(self, radio_id):
        c = self.conn.cursor()

        c.execute("SELECT {} FROM radios WHERE id={}".format(", ".join(Radio.FIELDS), radio_id))
        row = c.fetchone()
        if row is not None:
            radio = {}
            for i in range(len(Radio.FIELDS)):
                radio[Radio.FIELDS[i]] = row[i]

            return Radio(**radio)
        else:
            return None

    def addRadio(self, radio):
        c = self.conn.cursor()
        c.execute("INSERT INTO radios (name, uri, position) VALUES ('{}', '{}', {})".format(radio.name, radio.uri, radio.position))
        self.conn.commit()

    def deleteRadio(self, radio_id):
        c = self.conn.cursor()
        c.execute("DELETE FROM radios WHERE id={}".format(radio_id))
        self.conn.commit()

    def updateRadio(self, radio_id, name, uri, position):
        c = self.conn.cursor()
        c.execute("UPDATE radios SET name='{}', uri='{}', position='{}' WHERE id={}".format(name, uri, position, radio_id))
        self.conn.commit()




    def getRssFeeds(self):
        rss_feeds = []
        c = self.conn.cursor()
        for row in c.execute("SELECT {} FROM rss ORDER BY position".format(", ".join(RssFeed.FIELDS))):
            rss = {}
            for i in range(len(RssFeed.FIELDS)):
                rss[RssFeed.FIELDS[i]] = row[i]
            rss_feeds.append(RssFeed(**rss))

        return rss_feeds

    def getRssFeedsKeywordPosition(self):
        rss_feeds = {}
        c = self.conn.cursor()
        for row in c.execute("SELECT {} FROM rss".format(", ".join(RssFeed.FIELDS))):
            rss = {}
            for i in range(len(RssFeed.FIELDS)):
                rss[RssFeed.FIELDS[i]] = row[i]
            rss_feeds[rss["position"]] = RssFeed(**rss)

        return rss_feeds

    def getRss(self, rss_id):
        c = self.conn.cursor()

        c.execute("SELECT {} FROM rss WHERE id={}".format(", ".join(RssFeed.FIELDS), rss_id))
        row = c.fetchone()
        if row is not None:
            rss = {}
            for i in range(len(RssFeed.FIELDS)):
                rss[RssFeed.FIELDS[i]] = row[i]

            return RssFeed(**rss)
        else:
            return None

    def addRss(self, rss):
        c = self.conn.cursor()
        c.execute("INSERT INTO rss (name, uri, position) VALUES ('{}', '{}', {})".format(rss.name, rss.uri, rss.position))
        self.conn.commit()

    def deleteRss(self, rss_id):
        c = self.conn.cursor()
        c.execute("DELETE FROM rss WHERE id={}".format(rss_id))
        self.conn.commit()

    def updateRss(self, rss_id, name, uri, position):
        c = self.conn.cursor()
        c.execute("UPDATE rss SET name='{}', uri='{}', position='{}' WHERE id={}".format(name, uri, position, rss_id))
        self.conn.commit()

if __name__=="__main__":
    rbdb = RedBoxDataBase("redbox.db")

    print(rbdb.getRadios())
    rbdb.deleteRadio(1)
    print(rbdb.getRadios())
    
