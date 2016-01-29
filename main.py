#!/usr/bin/python
import sqlite3
import os.path

class Application:
    def __init__(self):

        """
        If master db doesn't exist, make the upload the master, and move on.
        """
        if not os.path.isfile("MarkTimeMaster.db"):
            os.rename("MarkTime.db", "MarkTimeMaster.db")
            return
        """
        Else...
        """

        self.conn = sqlite3.connect("MarkTimeMaster.db")
        self.c = self.conn.cursor()

        self.copyTable("attendance", "attendance1")
        self.execSQL("INSERT INTO attendance1 (boyID, attendance) VALUES (3, 2)")
        self.mergeTables("attendance", "attendance1")
        print("Merged stuff.")
        return

        self.execSQL("ATTACH DATABASE 'MarkTime.db' as upload;")
        self.execSQL("BEGIN;")
        self.execSQL("INSERT INTO boys (boyName, boySquad) SELECT boyName, boySquad FROM upload.boys;")
        self.execSQL("END;")
        self.execSQL("DETACH upload;" )

        self.conn.close()

    """
    Copies unique entries in tableB into tableA
    Unique entry defined by the key. If no key is supplied, first column (apart from _id)
    is assumed as the key.
    """
    def mergeTables(self, tableA, tableB, key=""):
        print("Merging tables.")
        cols = self.getColumns(tableA)
        del cols[0]
        if key == "":
            key = cols[0]
        print(cols*2)
        print(key)
        sql = "INSERT INTO "+tableA+" ("+",".join(cols)+") SELECT "+",".join(cols)+" FROM "+tableB+" WHERE "+key+" NOT IN (SELECT "+key+" FROM "+tableA+")"
        self.execSQL(sql)

        #self.c.execute("INSERT INTO "+tableA+" ("+(len(cols)*"?,")[:-1]+") "+
        #                "SELECT "+(len(cols)*"?,")[:-1]+" FROM "+tableB+" WHERE "+key+
        #                " NOT IN (SELECT "+key+" FROM "+tableA+");", (cols*2))
        self.conn.commit()

    def copyTable(self, tableName, newTableName):
        c = self.c.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='{}'".format(tableName))
        c = self.c.execute(c.fetchone()[0].replace(tableName, newTableName, 1))
        self.execSQL("INSERT INTO {} SELECT * FROM {};".format(newTableName, tableName))
        self.conn.commit()
        #self.c.execute()

    def renameTable(self, oldName, newName):
        self.copyTable(oldName, newName)
        self.execSQL("DROP TABLE {}".format(oldName))

    def getColumns(self, table):
        t = []
        for row in self.c.execute("PRAGMA table_info("+table+");"):
            t.append(row[1])
        return t

    def getTables(self):
        t = []
        for row in self.c.execute("SELECT name FROM sqlite_master WHERE type='table';"):
            t.append(row[0])
        return t

    def execSQL(self, sql):
        try:
            for row in self.c.execute(sql):
                print row
        except sqlite3.OperationalError  as e:
            print(e)

    def setFlag(self, flag):
        pass

if __name__ == "__main__":
    app = Application()