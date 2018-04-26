import pytest
import json
import os
import importlib
import jsonpickle
from fixture.application import Application
from fixture.db import DbFixture
from fixture.orm import ORMFixture

fixture = None
target = None


def load_config(file):
    global target
    if target is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file) as f:
            target = json.load(f)
    return target


@pytest.fixture
def app(request):

    global fixture
    browser = request.config.getoption("--browser")
    web_config = load_config(request.config.getoption("--target"))["web"]

    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, base_url=web_config["baseUrl"])

    fixture.session.ensure_login(username=web_config["username"], password=web_config["password"])
    return fixture


@pytest.fixture(scope="session", autouse=True)
def stop(request):

    def fin():
        fixture.session.ensure_logout()
        fixture.close()

    request.addfinalizer(fin)
    return fixture


@pytest.fixture(scope="session")
def db(request):
    db_config = load_config(request.config.getoption("--target"))["db"]
    dbfixture = DbFixture(host=db_config["host"], name=db_config["name"], user=db_config["user"], password=db_config["password"])

    def fin():
        dbfixture.close()

    request.addfinalizer(fin)
    return dbfixture


@pytest.fixture(scope="session")
def orm(request):
    db_config = load_config(request.config.getoption("--target"))["db"]
    ormfixture = ORMFixture(host=db_config["host"], name=db_config["name"], user=db_config["user"], password=db_config["password"])
    return ormfixture


@pytest.fixture
def check_ui(request):
    return request.config.getoption("--check_ui")


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--target", action="store", default="target.json")
    parser.addoption("--check_ui", action="store_true")


def pytest_generate_tests(metafunc):
    for fixture in metafunc.fixturenames:
        if fixture.startswith("data_"):
            test_data = load_from_module(fixture[5:])
            metafunc.parametrize(fixture, test_data, ids=[str(x) for x in test_data])
        elif fixture.startswith("json_"):
            test_data = load_from_json(fixture[5:])
            metafunc.parametrize(fixture, test_data, ids=[str(x) for x in test_data])


def load_from_module(module):
    return importlib.import_module("data.%s" % module).test_data


def load_from_json(file):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/%s.json" % file)) as f:
        return jsonpickle.decode(f.read())