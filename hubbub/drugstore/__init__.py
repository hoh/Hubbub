# Copyright (c) 2014 "Hugo Herter"
# [http://hugoherter.com]
#
# This file is part of Hubbub.
#
# Vega is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime
from .models import Message


def is_dummy(message):
    return message.startswith('?DUMMY:') \
        or message.startswith('<FONT>?DUMMY:')


def store(message, buddy, received=True):
    print('store... [{}]'.format(message))

    m = Message()

    m.length = len(message)
    m.date = datetime.now()
    m.dummy = is_dummy(message)
    m.received = received
    m.buddy = buddy

    m.save()
