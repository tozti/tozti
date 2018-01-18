import pytest
import os, sys, shutil

import tozti
import tozti.__main__
import tozti.app

from enum import Enum

class Ext_format(Enum):
    SERVER_FILE = 0
    SERVER_FOLDER = 1
    BAD_FORMAT = 2


@pytest.fixture(scope="function")
def empty_extensions_entry_leave(request):
    """
    Fixture that enable to clean `extensions/` folder before
    and after executing the test
    """
    def rmtree():
        for f in os.listdir("extensions/"):
            if f != ".gitkeep":
                shutil.rmtree(os.path.join("extensions", f))
    rmtree()
    request.addfinalizer(rmtree)


@pytest.mark.parametrize("extensions",
        [
            [("foo", Ext_format.SERVER_FILE, {"includes": ["a", "b"]})],
            [("foo", Ext_format.SERVER_FOLDER, {"includes": ["a", "b"]})],
            [("bar", Ext_format.BAD_FORMAT, {})],
            [("foo", Ext_format.SERVER_FILE, None)],
            [("foo", Ext_format.SERVER_FILE, None), ("bar", Ext_format.SERVER_FILE, {})],
            [("foo", Ext_format.SERVER_FILE, {}), ("bar", Ext_format.SERVER_FILE, {})],
        ]
        )
def test_find_exts(empty_extensions_entry_leave, extensions):
    """
    Test for find_exts function
    """
    # first, create the dummy extension
    # a dummy extension is parametrized as:
    #   - name, the name of the extension
    #   - add_single_file which is True if we want a server.py file, 
    #       otherwise a server/__init__.py file
    #   - manifest: the extension manifest. None if no manifest
    for name, ext_format, manifest in extensions:
        ext_path = os.path.join("extensions", name)
        os.mkdir(ext_path)
        file_path = "server.py"
        if ext_format == Ext_format.SERVER_FOLDER:
            file_path = "server/__init__.py"
            os.mkdir(os.path.join(ext_path, "server"))
        elif ext_format == Ext_format.BAD_FORMAT:
            file_path = "foo.py"
        file_path = os.path.join(ext_path, file_path)
        server_file = open(file_path, "w+")
        if manifest is not None:
            server_file.write("MANIFEST = {}".format(manifest))
        server_file.write("\n")
        server_file.close()

    # if one extension has a bad format, then the function raises something
    if any(e == Ext_format.BAD_FORMAT for _, e, _ in extensions):
        with pytest.raises(ValueError):
            list(tozti.__main__.find_exts())
    else:
        # get the outputted result and the expected result
        output = list(tozti.__main__.find_exts())
        expected = [tozti.app.Extension(name, **manifest) \
                for name, _, manifest in extensions   \
                if manifest is not None]

        # special equality function, we want the result to be the
        # same for __dict__ equality
        assert(len(output) == len(expected))
        for ext in output:
            exist_corresponding = False
            for ext2 in expected:
                exist_corresponding |= (ext.__dict__ == ext2.__dict__)
            assert(exist_corresponding)
