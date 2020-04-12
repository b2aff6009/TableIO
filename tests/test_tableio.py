import tableio as tio
import pytest

import os
import sys
import inspect
import json
current_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

baseSettings = {
    "type": "csv",
    "permission": "rw"
}


def test_createTableIOFactory():
    settings = baseSettings

    tests = [
        ["csv", tio.csvTableIO],
        ["xls", tio.xlsTableIO],
        ["google", tio.googleSheetTableIO]
    ]
    for test in tests:
        settings["type"] = test[0]
        myTableIO = tio.createTableIO(settings=settings)
        testTableIO = test[1](settings=settings)
        assert type(myTableIO) == type(
            testTableIO), "Wrong tableIO type was created. Created TableIO was: {}".format(type(myTableIO))


if __name__ == "__main__":
    test_createTableIOFactory()
