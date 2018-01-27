import subprocess
import os, sys, shutil
import pytest

def empty_extensions_list():
    for f in os.listdir("extensions/"):
        if f != ".gitkeep":
            shutil.rmtree(os.path.join("extensions", f))

def stop_tozti(tozti_proc):
    """
    Stop a given tozti_proc
    """
    if tozti_still_running(tozti_proc):
        tozti_proc.terminate()

def launch_tozti():
    """
    Start a tozti server and either:
        - return None if the server couldn't be launched
        - return a Popen object representing tozti's process
    """
    tozti_proc = subprocess.Popen(["python", "-m", "tozti", "dev"], 
                                  stdout = subprocess.PIPE)
    # parse stdout to know when the server is launched
    for line in iter(tozti_proc.stdout.readline, b''):
        if b'ERROR' in line \
           or b'CRITICAL' in line:
            stop_tozti(tozti_proc)
            return None
        if b'Finished boot sequence' in line:
            break
    return tozti_proc


def install_extension(ext):
    """ Install the extension `ext` (found in `tests/extension`)
    as a Tozti extension
    """
    extension_folder = "tests/extensions/"
    ext_test = os.path.join(extension_folder, ext)
    if os.path.isdir(ext_test):
        shutil.copytree(ext_test,
                        os.path.join("extensions/", ext))


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

def tozti_still_running(tozti):
    return tozti is not None and tozti.poll() is None
