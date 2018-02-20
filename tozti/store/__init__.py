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


#__all__ = ('UUID_RE', 'router', 'open_db', 'close_db', 'Store')

import logbook

from tozti.utils import APIError


logger = logbook.Logger('tozti.store')


class NoResourceError(APIError):
    code = 'NO_RESOURCE'
    title = 'resource not found'
    status = 404
    template = 'resource {id} not found'


class NoItemError(APIError):
    code = 'NO_ITEM'
    title = 'unknown body item'
    status = 400
    template = 'item {key} is unknown'


class BadItemError(APIError):
    code = 'BAD_ITEM'
    title = 'a body item is invalid'
    status = 400
    template = 'item {key} is invalid: {msg}'


class BadAttrError(BadItemError):
    code = 'BAD_ATTRIBUTE'
    title = 'an attribute is invalid'
    status = 400
    template = 'attribute {key} is invalid: {msg}'


class BadRelError(BadItemError):
    code = 'BAD_RELATIONSHIP'
    title = 'a relationship is invalid'
    status = 400
    template = 'relationship {key} is invalid: {msg}'


class NoTypeError(APIError):
    code = 'NO_TYPE'
    title = 'unknown type'
    status = 400
    template = 'type {type} is unknown'
