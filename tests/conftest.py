import pytest
from tests.commons import *


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
        stop_tozti(tozti)

    empty_extensions_list()
    #install extensions
    extensions_marker = request.node.get_marker("extensions")
    if extensions_marker is not None:
        for ext in extensions_marker.args:
            install_extension(ext)

    tozti = launch_tozti()

    yield tozti

    request.addfinalizer(tozti_end)


@pytest.fixture(scope="module")
def load_db(request):
    """Fixture that create a connection to the database and 
    close it when we are done

    Has the scope of a whole "module"
    """
    client = MongoClient(host="localhost", port=27017)
    yield client.tozti.resources, client.tozti.handles
    request.addfinalizer(lambda: client.close())


@pytest.fixture(scope="function")
def db(load_db):
    """Fixture loading a database and reset the content.
    This allows us to start a new test with an empty db
    """
    for collection in load_db:
        collection.drop()
    yield load_db[0]


@pytest.fixture
def firefox_options(firefox_options):
    """Fixture used with the headless browser
    """
    firefox_options.add_argument("-headless")
    return firefox_options
