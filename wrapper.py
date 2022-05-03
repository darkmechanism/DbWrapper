# TODO: Implement logging.

from sqlite3 import connect

class DbWrapper:
    def __init__(self, filename, log=""):
        self.__filename = filename
        self.__logfile = log

    def ShapeTable(self, paramarr, tablename):
        DbOverseer = connect(self.__filename)
        DbCursor = DbOverseer.cursor()
        DbCursor.execute(f"CREATE TABLE {tablename} ({', '.join(paramarr)})")
        DbOverseer.commit()
        DbOverseer.close()

    def AppendLine(self, paramarr, tablename):
        DbOverseer = connect(self.__filename)
        DbCursor = DbOverseer.cursor()
        temp = [f"'{i}'" for i in paramarr]
        DbCursor.execute(f"INSERT INTO {tablename} VALUES ({', '.join(temp)})")
        DbOverseer.commit()
        DbOverseer.close()

    def GetTable(self, tablename):
        DbOverseer = connect(self.__filename)
        DbCursor = DbOverseer.cursor()
        DbCursor.execute(f"SELECT * FROM {tablename}")
        LineInfo = DbCursor.fetchall()
        DbOverseer.commit()
        DbOverseer.close()
        return LineInfo

    def DeleteTable(self, tablename):
        DbOverseer = connect(self.__filename)
        DbCursor = DbOverseer.cursor()
        DbCursor.execute(f"DROP TABLE IF EXISTS {tablename}")
        DbOverseer.commit()
        DbOverseer.close()