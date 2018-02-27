import subprocess
import os, shutil
import time
import pytest
from tests.commons import tozti_still_running
import requests
from contextlib import contextmanager
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support.expected_conditions import staleness_of

def test_tozti_launch_and_runs(tozti):
    # check if tozti is running
    assert(tozti_still_running(tozti))

@pytest.mark.extensions("routing01")
def test_tozti_routing(tozti):
    # check if tozti is running
    answer = requests.get("http://127.0.0.1:8080/api/routing01/foo")
    assert(answer.text == "foo")
    assert(tozti_still_running(tozti))


@pytest.mark.extensions("bad_name")
def test_tozti_bad_name(tozti):
    # check if tozti is running
    assert(tozti_still_running(tozti))

"""
# vue routing
@pytest.mark.extensions("vue-routing01")
def test_tozti_vue_routing(selenium, tozti):
    assert(tozti_still_running(tozti))
    selenium.get("http://127.0.0.1:8080/counter")
    assert("test success" in selenium.page_source)

# vue menu item append
@pytest.mark.extensions("vue-menu-item01")
def test_tozti_vue_menu_item(selenium, tozti):
    assert(tozti_still_running(tozti))
    selenium.get("http://127.0.0.1:8080/")
    assert("test menu item" in selenium.page_source)
    assert(len(selenium.find_elements_by_xpath("//a[contains(text(), 'test menu item')]")) == 1)
"""

# test than loading a bad define type fails
@pytest.mark.extensions("type-baddefined01")
def test_tozti_bad_type(tozti):
    assert(not tozti_still_running(tozti))

# loading a well define type suceed
@pytest.mark.extensions("type-welldefined01")
def test_tozti_good_type(tozti):
    assert(tozti_still_running(tozti))
