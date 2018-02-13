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

from nacl.pwhash import (
    str as pwhash_str,
    verify as pwhash_verify)

from nacl.exceptions import InvalidkeyError as InvalidkeyError

import tozti

from tozti.auth.utils import BadPasswordError, create_macaroon
from tozti.utils import (RouterDef, NotJsonError, BadJsonError, json_response)

from tozti.auth import decorators
from pymacaroons import Macaroon, Verifier


router = RouterDef()
login = router.add_route('/login')
is_logged = router.add_route('/is_logged')
create_user = router.add_route('/create_user')

@login.post
@decorators.restrict_not_logged_in
async def login_post(req):
    if req.content_type != 'application/json':
        raise NotJsonError()
    try:
        data = await req.json()
        login = data['login']
        passwd = data['passwd']
    except (JSONDecodeError, IndexError, KeyError):
        raise BadJsonError()

    hash = await req.app['tozti-store'].hash_by_login(login)
    user_uid = await req.app['tozti-store'].user_uid_by_login(login)
    try:
        pwhash_verify(hash.encode('utf-8'), passwd.encode('utf-8'))
    except InvalidkeyError:
        raise BadPasswordError()

    rep = {'logged': True}
    
    if not tozti.PRODUCTION:
        rep['uid'] = str(user_uid)

    ans = json_response(rep)
    mac = create_macaroon({'login': login, 'uid': str(user_uid)})
    ans.set_cookie('auth-token', mac.serialize())
        
    return ans
    
@is_logged.get
@decorators.restrict_known_user
async def is_logged(req):
    return json_response({'logged':True})

@create_user.post
async def create_user(req):
    if req.content_type != 'application/json':
        raise NotJsonError()
    try:
        data = await req.json()
        login = data['login']
        name = data['name']
        passwd = data['passwd']
        email = data['email']
    except (JSONDecodeError, IndexError, KeyError):
        raise BadJsonError()

    uid_user = await req.app['tozti-store'].create({'data':{'type':'core/user', 'attributes':{
    	'name':name, 'login':login, 'email':email
    }}})
    hash = pwhash_str(passwd.encode('utf-8')).decode('utf-8')
    await req.app['tozti-store'].set_login_hash(login, hash)

    rep = {'created': True}

    if not tozti.PRODUCTION:
        rep['hash'] = hash
        rep['uid'] = str(uid_user)
        
    ans = json_response(rep)
    return ans
