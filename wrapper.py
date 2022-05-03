# TODO: Implement logging.

from sqlite3 import connect
from datetime import datetime


class Log:
    def __init__(self, filename):
        self.__filename = open(filename, "a")

    def plog(self, log):
        date = f'[{datetime.now().year}-{datetime.now().month}-{datetime.now().day}  {datetime.now().hour}.{datetime.now().minute}.{datetime.now().second}]'
        self.__filename.write(date + " " + log + "\n")

class DbWrapper:
    def __init__(self, filename, log):
        self.__filename = filename
        self.__logfile = Log(log)

    def ShapeTable(self, paramarr, tablename):
        DbOverseer = connect(self.__filename)
        DbCursor = DbOverseer.cursor()
        DbCursor.execute(f"CREATE TABLE {tablename} ({', '.join(paramarr)})")
        DbOverseer.commit()
        DbOverseer.close()
        self.__logfile.plog(f"{self.__filename}: Created table {tablename} with variables {paramarr}.")

    def AppendLine(self, paramarr, tablename):
        DbOverseer = connect(self.__filename)
        DbCursor = DbOverseer.cursor()
        temp = [f"'{i}'" for i in paramarr]
        DbCursor.execute(f"INSERT INTO {tablename} VALUES ({', '.join(temp)})")
        DbOverseer.commit()
        DbOverseer.close()
        self.__logfile.plog(f"{self.__filename}: Appended line to table {tablename} with variables {paramarr}.")

    def GetTable(self, tablename):
        DbOverseer = connect(self.__filename)
        DbCursor = DbOverseer.cursor()
        DbCursor.execute(f"SELECT * FROM {tablename}")
        LineInfo = DbCursor.fetchall()
        DbOverseer.commit()
        DbOverseer.close()
        self.__logfile.plog(f"{self.__filename}: Requested table {tablename}.")
        return LineInfo

    def UpdateVal(self, finderstat, setterstat, finder, setter, tablename):
        DbOverseer = connect(self.__filename)
        DbCursor = DbOverseer.cursor()
        sql = f''' UPDATE {tablename}
                  SET {setterstat} = ?
                  WHERE {finderstat} = ?'''
        DbCursor.execute(sql, (setter, finder))
        self.__logfile.plog(f"{self.__filename}: Updated {setterstat} to be {setter} in line where {finderstat} is {finder} in table {tablename}.")
        DbOverseer.commit()
        DbOverseer.close()

    def DeleteTable(self, tablename):
        DbOverseer = connect(self.__filename)
        DbCursor = DbOverseer.cursor()
        DbCursor.execute(f"DROP TABLE IF EXISTS {tablename}")
        DbOverseer.commit()
        DbOverseer.close()
        self.__logfile.plog(f"{self.__filename}: Deleted table {tablename}.")