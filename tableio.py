

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

    def setTable(self, name):
        pass

    def getValue(self, x, y):
        pass

    def setValue(self, x, y, value):
        pass


class csvTableIO(TableIO):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def setSheet(self, name):
        AssertionError("csv files don't contain tables")


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
        if x < 1 or y < 1:
            raise ValueError("Coordinates must be positive (>0) integers.")
        return self.table.cell(y, x).value

    def setValue(self, x, y, value):
        self.table.update_cell(y, x, value)

    def setTable(self, tableName):
        self.tableName = tableName
        self.table = self.sheet.worksheet(self.tableName)
