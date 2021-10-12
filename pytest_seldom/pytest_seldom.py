# Copyright (c) Microsoft Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import warnings
from datetime import datetime
from py.xml import html
from typing import Any, Callable, Dict, Generator, List, Optional

import pytest
from selenium import webdriver
from poium import Page
from poium.common import logging
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.opera import OperaDriverManager
from pytest_seldom.extend import ChromeDriverManager


# close color log (poium>1.0.2)
logging.colorLog = False


@pytest.fixture(scope="session")
def browser_type(browser_name: str):
    if browser_name == "chrome" or browser_name == "gc":
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    elif browser_name == "firefox" or browser_name == "ff":
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    elif browser_name == "safari":
        driver = webdriver.Safari()
    elif browser_name == "ie":
        driver = webdriver.Ie(executable_path=IEDriverManager().install())
    elif browser_name == "edge":
        driver = webdriver.Edge(executable_path=EdgeChromiumDriverManager().install())
    elif browser_name == "opera":
        driver = webdriver.Opera(executable_path=OperaDriverManager().install())
    else:
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    return driver


@pytest.fixture(scope="session")
def browser(browser_type, base_url: str):
    page = browser_type
    yield page
    page.quit()


@pytest.fixture(scope="session")
def page(browser_type, base_url: str):
    page = Page(browser_type)
    yield page
    browser_type.quit()


@pytest.fixture(scope="session")
def is_safari(browser_name: str) -> bool:
    return browser_name == "safari"


@pytest.fixture(scope="session")
def is_firefox(browser_name: str) -> bool:
    return browser_name == "firefox"


@pytest.fixture(scope="session")
def is_chrome(browser_name: str) -> bool:
    return browser_name == "chrome"


@pytest.fixture(scope="session")
def browser_name(pytestconfig: Any):
    browser_names = pytestconfig.getoption("--browser")
    if len(browser_names) == 0:
        return "chrome"
    if len(browser_names) == 1:
        return browser_names[0]
    warnings.warn(
        "When using unittest.TestCase specifying multiple browsers is not supported"
    )
    return browser_names[0]


def pytest_html_results_table_header(cells):
    cells.insert(2, html.th("Description"))
    cells.insert(1, html.th("Time", class_="sortable time", col="time"))
    cells.pop()


def pytest_html_results_table_row(report, cells):
    cells.insert(2, html.td(report.description))
    cells.insert(1, html.td(datetime.utcnow(), class_="col-time"))
    cells.pop()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
    extra = getattr(report, 'extra', [])
    if report.when == 'call':
        feature_request = item.funcargs['request']
        driver = feature_request.getfixturevalue('browser')
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            # only add additional html on failure
            img = driver.get_screenshot_as_base64()
            html_screenshot = """
            <div style="float: right;">
              <img src="data:image/jpg;base64,{img}" style="width: 350px; float: right; border-style: solid; border-width: 3px; border-color: #fa5c7c;"/>
            </div>
            """.format(img=str(img))
            extra.append(pytest_html.extras.html(html_screenshot))
        report.extra = extra


def pytest_addoption(parser: Any) -> None:
    group = parser.getgroup("seldom", "Seldom")
    group.addoption(
        "--browser",
        action="append",
        default=[],
        help="Browser engine which should be used",
    )

