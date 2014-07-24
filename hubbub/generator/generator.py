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

    def __init__(self, adapter, buddy_id, q_messages):
        self.adapter = adapter
        self.buddy_id = buddy_id
        self.q_messages = q_messages

    def run(self):
        while True:
            buddy = Buddy.get(id=self.buddy_id)
            if buddy.enabled:
                self.adapter.send_im_msg('?DUMMY:', buddy.identifier)
            sleep(5)


class Simulator(object):
    '''
        Simplisim Generator simulator class.
    '''

    def __init__(self, real_messages):
        self.real_messages = real_messages

    def date_boundaries(self):
        """Returns the begin and end datetimes for the simulation.
        Currently the beginning of the day of the first message and the end
        of the day of the last message."""

        r = self.real_messages
        start = datetime.combine(r[0][0], datetime.min.time())
        end = datetime.combine(r[-1][0], datetime.max.time())
        #print('start:', start)
        #print('end:', end)
        return start, end

    def run(self):
        dummy_messages = []

        start, end = self.date_boundaries()

        t = start
        while t < end:
            dummy_messages.append((t, 10))
            t += timedelta(seconds=5)

        return dummy_messages
