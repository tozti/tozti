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

import tozti
import tozti.auth.utils

from pysodium import (crypto_pwhash_scryptsalsa208sha256_str,
                      crypto_pwhash_scryptsalsa208sha256_str_verify)
import json
from json import JSONDecodeError
from tozti.utils import (RouterDef, NotJsonError, BadJsonError,
                         json_response)
from tozti.core_schemas import SCHEMAS

router = RouterDef()
login = router.add_route('/login')

@login.get
async def login_get(req):
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

    userPasswdList = await req.app['tozti-store'].find_fields(SCHEMAS['user_password'], login=login)

    if len(userPasswdList) == 0:
        raise tozti.auth.utils.BadPasswordError()
    
    localHash = userPasswd['hash']

    try:
        pysodium.crypto_pwhash_scryptsalsa208sha256_str_verify(
            localHash, passwd
        )
    except ValueError:
        raise tozti.auth.utils.BadPasswordError()
        
    ans = json_response({'logged':True})
    mac = tozti.auth.utils.create_macaroon({'login':login, 'id':43})
    ans.set_cookie('test', mac.serialize())
    return ans
    
