import subprocess
import time
import pytest
import tests.commons as commons

@pytest.fixture(scope="function")
def tozti(request):
    """
    Fixture that:
        - clean the extension folder
        - launch a tozti server
        - waits one second for it to be started
        - shutdown it at the end
    """
    commons.empty_extensions_list()
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
