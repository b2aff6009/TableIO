import gspread
from gspread.models import Cell
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
        self.debug = self.settings.get("debug",0)
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

    def getData(self, x, y, xend, yend):
        pass

    def row(self, x, y, values):
        pass

    def col(self, x, y, values):
        pass
    
    def data(self, x, y, values):
        '''takes a list of lists as input and writes it from top left to bottom right (liniewise)'''
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
        line = self.table[y-1]
        if len(line) <= x-1:
            return ""
        return line[x-1]


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
        self.cache = {}
        if "credentialPath" in self.settings.keys():
            self.scope = ['https://spreadsheets.google.com/feeds',
                          'https://www.googleapis.com/auth/drive']
            self.creds = ServiceAccountCredentials.from_json_keyfile_name(
                self.settings["credentialPath"], self.scope)
            self.client = gspread.authorize(self.creds)
            self.sheet = self.client.open(self.settings["spreadsheet"])
            #self.allsheets = self.client.openall()
            self.setTable(self.settings["table"])
        elif self.table != None:
            AssertionError("Neither credentials are given nor a spreadsheet.")


    def getValue(self, x, y):
        super().permissionCheck("r")
        super().intCheck(x,y)
        if x  in self.cache.keys():
            if y in self.cache[x].keys():
                return self.cache[x][y]
        return self.table.cell(y, x).value


    def setValue(self, x, y, value):
        super().permissionCheck("w")
        super().intCheck(x,y)
        self.table.update_cell(y, x, value)


    def setTable(self, tableName):
        try:
            worksheet = self.sheet.worksheet(tableName)
        except:
            if self.debug > 0:
                print("TableIO: {} was not found.".format(tableName))
            template = self.settings.get("template", 0)
            if template == 0:
                self.sheet.duplicate_sheet(0, insert_sheet_index=1, new_sheet_name=tableName)
            else:
                sheets = self.sheet.worksheets()
                for sheet in self.sheet.worksheets():
                    if sheet.title == template:
                        self.sheet.duplicate_sheet(sheet.id, insert_sheet_index=1, new_sheet_name=tableName)
                        break

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

    def getData(self, x, y, xend, yend):
        super().permissionCheck("r")
        super().intCheck(x,y, xend, yend) 

        xbegin = chr(ord('A')-1+x)
        xendStr = chr(ord(xbegin) + xend- 1)
        rangeStr = '{}{}:{}{}'.format(xbegin,y,xendStr,yend)
        cell_list = self.table.range(rangeStr)

        xdiff = xend - x
        result = []
        for i, cell in enumerate(cell_list):
            if (i%(xdiff+1) == 0):
                result.append([])
            result[-1].append(cell.value)

        return result

    def cacheArea(self, x, y, xend, yend, updateRate = 0):
        data = self.getData(x,y, xend, yend)
        for i, col in enumerate(data):
            for j, celldata in enumerate(col):
                if j+y not in self.cache.keys(): 
                    self.cache[j+y]= {}
                #if i+x not in self.cache.keys(): 
                #    self.cache[i+x]= {}
                self.cache[j+y][i+x] = celldata
                #self.cache[i+x][j+y] = celldata



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


    def data(self, x, y, values):
        super().permissionCheck("w")

        cells = []
        for j, line in enumerate(values,y):
            for i, val in enumerate(line, x):
                cells.append(Cell(row=j, col=i, value=val))
        self.table.update_cells(cells)
