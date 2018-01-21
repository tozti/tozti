import subprocess
import os, shutil
import time
import pytest
import tests.commons as commons
import requests

@pytest.fixture(scope="function")
def tozti(request):
    """
    Fixture that:
        - clean the extension folder
        - if extensions are to be installed, install the extensions
        - launch a tozti server
        - waits one second for it to be started
        - shutdown it at the end
    To install extensions, add a mark named "extensions" to the test 
    with arguments the extensions you want to install:
        `@pytest.mark.extensions("ext1", "ext2")`
    """
    def tozti_end():
        if tozti.poll() is None:
            tozti.terminate()

    commons.empty_extensions_list()
    #install extensions
    extensions_marker = request.node.get_marker("extensions")
    if extensions_marker is not None:
        extension_folder = "tests/extensions/"
        for ext in extensions_marker.args:
            ext_test = os.path.join(extension_folder, ext)
            if os.path.isdir(ext_test):
                shutil.copytree(ext_test,
                                os.path.join("extensions/", ext))

        # install the exensions
    tozti = subprocess.Popen(["python", "-m", "tozti", "dev"], stdout = subprocess.PIPE)
    # parse stdout to know when the server is launched
    for line in iter(tozti.stdout.readline, b''):
        if b'ERROR' in line:
            tozti_end()
            assert(False)
        if b'Finished boot sequence' in line:
            break

    yield tozti

    request.addfinalizer(tozti_end)

def test_tozti_launch_and_runs(tozti):
    # check if tozti is running
    assert(tozti.poll() is None)

@pytest.mark.extensions("routing01")
def test_tozti_routing(tozti):
    # check if tozti is running
    answer = requests.get("http://0.0.0.0:8080/api/routing01/foo")
    assert(answer.text == "foo")
    assert(tozti.poll() is None)

