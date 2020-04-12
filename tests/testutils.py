
import os
import sys
import inspect
import json
current_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import tableio as tio


def read_data(baseSettings, tests):
    testTableIO = tio.createTableIO(settings=baseSettings)
    for test in tests:
        settings = dict(baseSettings)
        for key, val in test[0].items():
            settings[key] = val
        value = testTableIO.getValue(test[0]["x"], test[0]["y"])
        assert test[1] == value, "Expected value: {} got {}".format(
            value, test[1])


def read_from_two_tables(baseSettings, tests):
    testTableIO = tio.createTableIO(settings=baseSettings)
    for test in tests:
        settings = dict(baseSettings)
        for key, val in test[0].items():
            settings[key] = val
        testTableIO.setTable(settings["table"])
        value = testTableIO.getValue(test[0]["x"], test[0]["y"])
        assert test[1] == value, "Expected value: {} got {}".format(
            value, test[1])


def write_data(baseSettings, tests):
    testTableIO = tio.createTableIO(settings=baseSettings)
    for test in tests:
        settings = dict(baseSettings)
        for key, val in test[0].items():
            settings[key] = val
        testTableIO.setTable(settings["table"])

        # Clear cell value
        testTableIO.setValue(test[0]["x"], test[0]["y"], "")
        value = testTableIO.getValue(test[0]["x"], test[0]["y"])
        assert "" == value, "Expected value: {} got {}".format(value, test[1])

        testTableIO.setValue(test[0]["x"], test[0]["y"], test[1])
        value = testTableIO.getValue(test[0]["x"], test[0]["y"])
        assert test[1] == value, "Expected value: {} got {}".format(
            value, test[1])

def permission_test(baseSettings, tests):

    for test in tests:
        settings = dict(baseSettings)
        testTableIO = tio.createTableIO(settings=settings)
        for key, val in test[0].items():
            settings[key] = val
        testTableIO.setTable(settings["table"])
        x = settings["x"]
        y = settings["y"]

        try:
            value = testTableIO.setValue(x, y, test[1])
            assert "w" in settings["permission"], "Set value without permission to write."
        except PermissionError:
            assert "w" not in settings["permission"], "Faild to getValue."

        try:
            value = testTableIO.getValue(x, y)
            assert test[1] == value, "Expected value: {} got {}".format(
                value, test[1])
            assert "r" in settings["permission"], "Got value without permission to read."
        except PermissionError:
            assert "r" not in settings["permission"], "Got permission error."


            