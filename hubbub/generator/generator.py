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

from __future__ import print_function

from time import sleep
from datetime import datetime, timedelta

from hubbub.drugstore.models import Buddy


class Generator(object):
    '''
        Simplisim Generator class.
    '''

    def __init__(self, adapter, q_messages):
        self.adapter = adapter
        self.q_messages = q_messages

    def run(self):
        while True:
            self.adapter.send_im_msg('?DUMMY:')
            buddy = Buddy.get(alias='carol')
            self.adapter.send_im_msg('?DUMMY:', buddy.identifier)
            sleep(5)


class Simulator(object):
    '''
        Simplisim Generator simulator class.
    '''

    def __init__(self, real_messages):
        self.real_messages = real_messages

    def run(self):
        dummy_messages = []

        r = self.real_messages
        start = datetime.combine(r[0]['date'], datetime.min.time())
        end = datetime.combine(r[0]['date'], datetime.max.time())
        print('start:', start)
        print('end:', end)

        t = start
        while t < end:
            dummy_messages.append({'date': t})
            t += timedelta(seconds=5)

        return dummy_messages
