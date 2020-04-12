
import pytest

import testutils as tu

baseSettings = {
    "type": "google",
    "permission": "rw",
    "table": "Test1",
    # GoogleCrawler Settings
    "credentialPath": "./dummy-credentials.json",
    "spreadsheet": "Dummy1"
}

readTests = [
    [{"x": 1, "y": 1}, "1"],
    [{"x": 1, "y": 2}, "2"],
    [{"x": 2, "y": 1}, "11"]
]

@pytest.mark.skip(reason="Can't be tested without credentials")
def test_read_data():
    tu.read_data(baseSettings, readTests)


@pytest.mark.skip(reason="Can't be tested without credentials")
def test_read_from_two_tables():
    addTests = [
        [{"table": "Test2", "x": 1, "y": 1}, "A"],
        [{"table": "Test2", "x": 1, "y": 2}, "B"],
        [{"table": "Test2", "x": 2, "y": 1}, "a"],
    ]
    readTests.extend(addTests)
    tu.read_from_two_tables(baseSettings, readTests)


writeTests = [
    [{"table": "Test3", "x": 1, "y": 1}, "h"],
    [{"table": "Test3", "x": 1, "y": 2}, "H"],
    [{"table": "Test3", "x": 2, "y": 1}, "i"],
]

@pytest.mark.skip(reason="Can't be tested without credentials")
def test_write_data():
    tu.write_data(baseSettings, writeTests)


readRowTests = [
    [{"table": "Test1", "x": 1, "y": 1, "len": 3}, ["1", "11", "21"]],
    [{"table": "Test1", "x": 1, "y": 2, "len": 3}, ["2", "12", "22"]],
    [{"table": "Test1", "x": 2, "y": 2, "len": 2}, ["12", "22"]],
    [{"table": "Test1", "x": 1, "y": 1, "len": 0}, []],
    [{"table": "Test1", "x": 1, "y": 1, "len": -1}, []],
]
@pytest.mark.skip(reason="Can't be tested without credentials")
def test_read_row():
    tu.read_row(baseSettings, readRowTests)


readColTests = [
    [{"table": "Test1", "x": 1, "y": 1, "len": 3}, ["1", "2", "3"]],
    [{"table": "Test1", "x": 2, "y": 1, "len": 3}, ["11", "12", "13"]],
    [{"table": "Test1", "x": 3, "y": 3, "len": 2}, ["23", "24"]],
    [{"table": "Test1", "x": 1, "y": 1, "len": 0}, []],
    [{"table": "Test1", "x": 1, "y": 1, "len": -1}, []],
]
@pytest.mark.skip(reason="Can't be tested without credentials")
def test_read_col():
    tu.read_col(baseSettings, readColTests)

writeRowTests= [
    [{"table": "Test3", "x": 1, "y": 6}, ["W", "E", "R", "T"]],
]

@pytest.mark.skip(reason="Can't be tested without credentials")
def test_write_row():
    tu.write_row(baseSettings, writeRowTests)

writeColTests= [
    [{"table": "Test3", "x": 6, "y": 1}, ["W", "E", "R", "T"]],
]

@pytest.mark.skip(reason="Can't be tested without credentials")
def test_write_col():
    tu.write_col(baseSettings, writeColTests)

permissionTests = [
    [{"table": "Test2", "permission": "r", "x": 1, "y": 1}, "A"],
    [{"table": "Test3", "permission": "w", "x": 1, "y": 1}, "k"],
    [{"table": "Test2", "permission": "", "x": 1, "y": 1}, "x"],
    [{"table": "Test3", "permission": "rw", "x": 1, "y": 1}, "j"]
]

@pytest.mark.skip(reason="Can't be tested without credentials")
def test_permissions():
    tu.permission_test(baseSettings, permissionTests)


if __name__ == "__main__":
    #test_read_col()
    #test_read_row()
    test_write_col()
    test_write_row()