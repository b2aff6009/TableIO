

def createTableIO(settings, callback = None):
    selector = {
        "csv" : csvTableIO,
        "google" : googleSheetTableIO,
        "xls" : xlsTableIO
    }
    return selector[settings.get("type", "csv")](settings, callback)


class TableIO:
    def __init__(self, settings, callback = None):
        self.settings = settings
        self.callback = callback

class csvTableIO(TableIO):
    def __init__(self, settings, callback=None):
        super().__init__(settings, callback=callback)


class xlsTableIO(TableIO):
    def __init__(self, settings, callback=None):
        super().__init__(settings, callback=callback)

class googleSheetTableIO(TableIO):
    def __init__(self, settings, callback=None):
        super().__init__(settings, callback=callback)