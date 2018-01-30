from tests.commons import tozti

def test_macaroon(tozti):

    from tozti.cookie.utils import create_macaroon
    
    mac = create_macaroon('test', 42, {1:7, 2:9, 3:7}, coucou=2, salut='coucou')
    print(mac.inspect())
        
