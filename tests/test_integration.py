import subprocess
import os, shutil
import time
import pytest
from tests.commons import tozti, tozti_still_running
import requests


def test_tozti_launch_and_runs(tozti):
    # check if tozti is running
    assert(tozti_still_running(tozti))

@pytest.mark.extensions("routing01")
def test_tozti_routing(tozti):
    # check if tozti is running
    answer = requests.get("http://0.0.0.0:8080/api/routing01/foo")
    assert(answer.text == "foo")
    assert(tozti_still_running(tozti))



# test using headerless browser
@pytest.fixture
def firefox_options(firefox_options):
    firefox_options.add_argument("-headless")
    return firefox_options

# vue routing
@pytest.mark.extensions("vue-routing01")
def test_tozti_vue_routing(selenium, tozti):
    assert(tozti_still_running(tozti))
    selenium.get("http://0.0.0.0:8080/counter")
    assert("test success" in selenium.page_source)

# test than loading a bad define type fails
@pytest.mark.extensions("type-baddefined01")
def test_tozti_bad_type(tozti):
    assert(not tozti_still_running(tozti))

# loading a well define type suceed
@pytest.mark.extensions("type-welldefined01")
def test_tozti_good_type(tozti):
    assert(tozti_still_running(tozti))
