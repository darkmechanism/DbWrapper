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

    def DeleteTable(self, tablename):
        DbOverseer = connect(self.__filename)
        DbCursor = DbOverseer.cursor()
        DbCursor.execute(f"DROP TABLE IF EXISTS {tablename}")
        DbOverseer.commit()
        DbOverseer.close()
        self.__logfile.plog(f"{self.__filename}: Deleted table {tablename}.")

    
Test = DbWrapper("main.db", "logs.txt")

Test.ShapeTable(["ip", "port"], "netinfo")
Test.AppendLine(["192.168.1.1", "80"], "netinfo")
print(Test.GetTable("netinfo"))