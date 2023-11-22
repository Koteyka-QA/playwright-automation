import logging
import os
from settings import *
from pytest import fixture
from playwright.sync_api import sync_playwright
from page_object.application import App


@fixture(autouse=True, scope='session')
def preconditions():
    logging.info('precondition started')
    yield
    logging.info('postcondition started')


@fixture(scope='session')
def get_playwright():
    with sync_playwright() as playwright:
        yield playwright


@fixture(scope='session', params=['chromium'])
def get_browser(get_playwright, request):
    browser = request.param
    os.environ['BROWSER'] = browser
    headless = request.config.getini('headless')
    if headless == 'True':
        headless = True
    else:
        headless = False

if browser == 'chromium':
    bro = get_playwright.chromium.launch(headless=headless)



@fixture(scope='session')
def desktop_app(get_browser, request):
    base_url = request.config.getini("base_url")
    app: App = App(get_browser, base_url=base_url, **BROWSER_OPTIONS)
    app.goto('/')
    yield app
    app.close()


@fixture(scope='session')
def desktop_app_auth(desktop_app, request):
    secure = request.config.getoption('--secure')
    config = load_config(secure)
    desktop_app.goto('/login')
    desktop_app.login(**config)
    yield app


@fixture(scope='session')
def mobile_app(get_playwright, get_browser):
    base_url = get_browser.getini('base_url')
    device = get_browser.config.getoption('--device')
    device_config = get_playwright.devices.get(device)
    if device_config is not None:
        device_config.update(BROWSER_OPTIONS)
    else:
        device_config = BROWSER_OPTIONS
    app = App(get_browser, base_url=base_url, **device_config)
    app.goto('/')
    yield app
    app.close()


@fixture(scope='session')
def mobile_app_auth(mobile_app, request):
    secure = request.config.getoption('--secure')
    config = load_config(secure)
    mobile_app.goto('/login')
    mobile_app.login(**config)
    yield desktop_app


def pytest_addoption(parser):
    parser.addoption('--secure', action='store', default='secure.json')
    parser.addoption('--device', action='store', default='')
    parser.addoption('--browser', action='store', default='chromium')
    parser.addoption('--headless', action='store_true', help='run browser in headless mode')
    parser.addini('base_url', help='base url of site under test', default='http://127.0.0.1:8000')



def load_config(file):
    config_file = os.path.abspath(os.path.join(os.path.dirname(__file__), file))
    with open(config_file) as cfg:
        return json.loads(cfg.read())
