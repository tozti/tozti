# -*- coding:utf-8 -*-

# This file is part of Tozti.

# Tozti is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Tozti is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with Tozti.  If not, see <http://www.gnu.org/licenses/>.


from json import JSONDecodeError

from pysodium import (
    crypto_pwhash_scryptsalsa208sha256_str as pwhash_str,
    crypto_pwhash_scryptsalsa208sha256_str_verify as pwhash_verify)

from tozti.auth.utils import BadPasswordError, create_macaroon
from tozti.utils import (RouterDef, NotJsonError, BadJsonError, json_response)


router = RouterDef()
login = router.add_route('/login')

@login.post
async def login_post(req):
    if req.content_type != 'application/json':
        raise NotJsonError()
    try:
        data = await req.json()
        login = data['login']
        passwd = data['passwd']
    except JSONDecodeError:
        raise BadJsonError()
    except IndexError:
        raise BadJsonError()

    (uid, hash) = await req.app['tozti-store'].hash_by_login(login)

    try:
        pwhash_verify(hash, passwd)
    except ValueError:
        raise BadPasswordError()
        
    ans = json_response({'logged': True})
    mac = create_macaroon({'login': login, 'id': 43})
    ans.set_cookie('test', mac.serialize())
    return ans
    
