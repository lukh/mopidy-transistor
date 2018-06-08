import sqlite3 as lite
import os

class Radio(object):
    FIELDS = ["id", "name", "uri", "position"]
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return "Radio <{}, {}, {}, {}>".format(self.id, self.name, self.uri, self.position)


class RedBoxDataBase(object):
    def __init__(self, filename):
        db_exists = os.path.isfile(filename)

        self.conn = lite.connect(filename)

        if not db_exists:
            self.initDb()


    def initDb(self):
        c = self.conn.cursor()
        c.execute("CREATE TABLE radios ( id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, name	TEXT, uri	TEXT,  position	REAL  );")
        self.conn.commit()


    def getRadios(self):
        
        radios = []
        c = self.conn.cursor()
        for row in c.execute("SELECT {} FROM radios".format(", ".join(Radio.FIELDS))):
            radio = {}
            for i in range(len(Radio.FIELDS)):
                radio[Radio.FIELDS[i]] = row[i]
            radios.append(Radio(**radio))

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

if __name__=="__main__":
    rbdb = RedBoxDataBase("redbox.db")

    print(rbdb.getRadios())
    rbdb.deleteRadio(1)
    print(rbdb.getRadios())
    