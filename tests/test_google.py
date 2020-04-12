
import pytest

import testutils as tu

baseSettings = {
    "type": "google",
    "parse": False,
    "parseDirection": "row",
    "offsetX": 0,
    "offsetY": 0,
    "permission": "",
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


if __name__ == "__main__":
    test_write_data()
