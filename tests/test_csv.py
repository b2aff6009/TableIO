

import pytest

import testutils as tu

baseSettings = {
    "type": "csv",
    "permission": "rw",
    "table": "Test1",
    #csv settings
    "path": "./tests/testdata/test1.csv",
    "delimiter": ";"
}


readTests = [
    [{"x": 1, "y": 1}, "1"],
    [{"x": 1, "y": 2}, "2"],
    [{"x": 2, "y": 1}, "11"]
]

def test_read_data():
    tu.read_data(baseSettings, readTests)

readRowTests = [
    [{"x": 1, "y": 1, "len": 3}, ["1", "11", "21"]],
    [{"x": 1, "y": 2, "len": 3}, ["2", "12", "22"]],
    [{"x": 2, "y": 2, "len": 2}, ["12", "22"]],
    [{"x": 1, "y": 1, "len": 0}, []],
    [{"x": 1, "y": 1, "len": -1}, []],
]
def test_read_row():
    tu.read_row(baseSettings, readRowTests)


readColTests = [
    [{"x": 1, "y": 1, "len": 3}, ["1", "2", "3"]],
    [{"x": 2, "y": 1, "len": 3}, ["11", "12", "13"]],
    [{"x": 3, "y": 3, "len": 2}, ["23", "24"]],
    [{"x": 1, "y": 1, "len": 0}, []],
    [{"x": 1, "y": 1, "len": -1}, []],
]
def test_read_col():
    tu.read_col(baseSettings, readColTests)


writeTests = [
    [{"path": "./tests/testdata/test3.csv", "x": 1, "y": 1}, "h"],
    [{"path": "./tests/testdata/test3.csv", "x": 1, "y": 2}, "H"],
    [{"path": "./tests/testdata/test3.csv", "x": 2, "y": 1}, "i"],
]
def test_write_data():
    tu.write_data(baseSettings, writeTests)


writeRowTests= [
    [{"path": "./tests/testdata/test3.csv", "x": 1, "y": 6}, ["W", "E", "R", "T"]],
]

def test_write_row():
    tu.write_row(baseSettings, writeRowTests)

writeColTests= [
    [{"path": "./tests/testdata/test3.csv", "x": 6, "y": 1}, ["W", "E", "R", "T"]],
]

def test_write_col():
    tu.write_col(baseSettings, writeColTests)

if __name__ == "__main__":
    #test_read_data()
    test_read_col()
    #test_read_row()

    #test_write_data()
    #test_write_col()
    #test_write_row()