

import gspread
from oauth2client.service_account import ServiceAccountCredentials


def createTableIO(**kwargs):
    selector = {
        "csv": csvTableIO,
        "google": googleSheetTableIO,
        "xls": xlsTableIO
    }
    return selector[kwargs["settings"].get("type", "csv")](**kwargs)


class TableIO:
    def __init__(self, **kwargs):
        self.settings = kwargs["settings"]
        self.callback = kwargs.get("callback", None)
        self.sheet = kwargs.get("sheet", None)
        self.table = kwargs.get("table", None)

    def permissionCheck(self, perm):
        verb = {"r": "read", "w": "write"}
        if perm not in self.settings["permission"]:
            raise PermissionError("Missing permisson to {}.".format(verb[perm]))

    def intCheck(self, *args):
        for value in args:
            if value < 1:
                raise ValueError("Value must be positive (>0) integers.")

    def setTable(self, name):
        pass

    def getValue(self, x, y):
        pass

    def setValue(self, x, y, value):
        pass

    def getCol(self, x, y, length):
        pass

    def getRow(self, x, y, length):
        pass

    def row(self, x, y, values):
        pass

    def col(self, x, y, values):
        pass

import csv
from chardet import detect
class csvTableIO(TableIO):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        path = self.settings["path"]
        self.table = [] 
        self.loadedLines = 0

        if ("r" in self.settings["permission"]):
            csvfile = open(path, mode = "r", encoding=self.get_encoding_type(path))
            self.reader = csv.reader(csvfile, delimiter=self.settings["delimiter"])
            #for row in self.reader:
            #    print(row)

        if ("w" in self.settings["permission"]):
            csvfile = open(path, mode = "a", encoding=self.get_encoding_type(path))
            self.writer = csv.writer(csvfile, delimiter=self.settings["delimiter"])


    def get_encoding_type(self, file):
        with open(file, 'rb+') as f:
            rawdata = f.read()
        return detect(rawdata)['encoding']

    def loadLine(self):
        self.loadedLines += 1
        try:
            line = next(self.reader)
        except StopIteration:
            line = []
        self.table.append(line)
        return line


    def setSheet(self, name):
        AssertionError("csv files don't contain tables")

    def getValue(self, x, y):
        super().permissionCheck("r")
        super().intCheck(x,y)
        while y >= self.loadedLines:
            self.loadLine()
        return self.table[y-1][x-1]


    def setValue(self, x, y, value):
        super().permissionCheck("w")
        super().intCheck(x,y)

    def getCol(self, x, y, length):
        super().permissionCheck("r")
        super().intCheck(x,y, length)
        while y+length >= self.loadedLines:
            self.loadLine()
        lines = self.table[y-1:y-1+length]
        return [line[x-1] for line in lines]

    def getRow(self, x, y, length):
        super().permissionCheck("r")
        super().intCheck(x,y, length)
        while y >= self.loadedLines:
            self.loadLine()
        return self.table[y-1][x-1:x-1+length]

    def row(self, x, y, values):
        super().permissionCheck("w")
        super().intCheck(x,y)

    def col(self, x, y, values):
        super().permissionCheck("w")
        super().intCheck(x,y)


class xlsTableIO(TableIO):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class googleSheetTableIO(TableIO):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if "credentialPath" in self.settings.keys():
            self.scope = ['https://spreadsheets.google.com/feeds',
                          'https://www.googleapis.com/auth/drive']
            self.creds = ServiceAccountCredentials.from_json_keyfile_name(
                self.settings["credentialPath"], self.scope)
            self.client = gspread.authorize(self.creds)
            self.sheet = self.client.open(self.settings["spreadsheet"])
            self.setTable(self.settings["table"])
        elif self.table != None:
            AssertionError("Neither credentials are given nor a spreadsheet.")


    def getValue(self, x, y):
        super().permissionCheck("r")
        super().intCheck(x,y)
        return self.table.cell(y, x).value


    def setValue(self, x, y, value):
        super().permissionCheck("w")
        super().intCheck(x,y)
        self.table.update_cell(y, x, value)


    def setTable(self, tableName):
        self.tableName = tableName
        self.table = self.sheet.worksheet(self.tableName)


    def getCol(self, x, y, length):
        super().permissionCheck("r")
        super().intCheck(x,y, length)

        x = chr(ord('A')-1+x)
        yend = y + length - 1
        rangeStr = '{}{}:{}{}'.format(x,y,x,yend)
        cell_list = self.table.range(rangeStr)

        result = []
        for cell in cell_list:
            result.append(cell.value)
        return result


    def getRow(self, x, y, length):
        super().permissionCheck("r")
        super().intCheck(x,y, length)

        xbegin = chr(ord('A')-1+x)
        xend = chr(ord(xbegin) + length - 1)
        rangeStr = '{}{}:{}{}'.format(xbegin,y,xend,y)
        cell_list = self.table.range(rangeStr)

        result = []
        for cell in cell_list:
            result.append(cell.value)
        return result


    def writeRange(self, rangeStr, values):
        cell_list = self.table.range(rangeStr)

        for i, val in enumerate(values):
            cell_list[i].value = val
        self.table.update_cells(cell_list)


    def col(self, x, y, values):
        super().permissionCheck("w")

        x = chr(ord('A')-1+x)
        yend = y + len(values)
        rangeStr = '{}{}:{}{}'.format(x, y, x, yend)
        self.writeRange(rangeStr, values)


    def row(self, x, y, values):
        super().permissionCheck("w")

        x = chr(ord('A')-1+x)
        xend = chr(ord(x)+len(values))
        rangeStr = '{}{}:{}{}'.format(x,y,xend, y)
        self.writeRange(rangeStr, values)