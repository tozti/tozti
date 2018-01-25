import subprocess
import os, shutil
import time
import pytest
from tests.commons import tozti
import requests


def test_tozti_launch_and_runs(tozti):
    # check if tozti is running
    assert(tozti.poll() is None)

@pytest.mark.extensions("routing01")
def test_tozti_routing(tozti):
    # check if tozti is running
    answer = requests.get("http://0.0.0.0:8080/api/routing01/foo")
    assert(answer.text == "foo")
    assert(tozti.poll() is None)



# test using headerless browser
@pytest.fixture
def firefox_options(firefox_options):
    firefox_options.add_argument("-headless")
    return firefox_options

# vue routing
@pytest.mark.extensions("vue-routing01")
def test_tozti_vue_routing(selenium, tozti):
    selenium.get("http://0.0.0.0:8080/counter")
    assert("test success" in selenium.page_source)
