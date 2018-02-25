import pytest
from tests.commons import make_call
from tozti.auth.__init__ import login_post, create_user

def test_macaroon():
    from tozti.auth.utils import create_macaroon
    from tozti.__main__ import load_config_file
    import tozti as tozti_app
    
    tozti_app.CONFIG = load_config_file()
    
    mac = create_macaroon('test', 42, {1:7, 2:9, 3:7}, coucou=2, salut='coucou')

