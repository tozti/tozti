import subprocess
import time
import pytest
import tests.commons as commons

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
    commons.empty_extensions_list()
    extensions_marker = request.node.get_marker("extensions")
    if extensions_marker is not None:
        print(extensions_marker.args)
        # install the exensions
    tozti = subprocess.Popen(["python", "-m", "tozti", "dev"])
    time.sleep(1)

    yield tozti

    def tozti_end():
        if tozti.poll() is None:
            tozti.terminate()
    request.addfinalizer(tozti_end)

def test_tozti_launch_and_runs(tozti):
    # check if tozti is running
    assert(tozti.poll() is None)
