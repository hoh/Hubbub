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

from random import random, gauss
from time import sleep
from Queue import Empty

from hubbub.drugstore.models import Buddy


class HeartBeatGenerator(object):
    '''
        Generates new messages at relatively constant time intervals.
        (relatively = random around an average)
    '''
    period = 2  # average period between messages, in seconds

    def __init__(self, adapter, q_messages):
        self.adapter = adapter
        self.q_messages = q_messages

    def run(self):
        while True:
            print('generator: new loop')
            delay = random() * self.period * 2
            try:
                # We get a real message
                # TODO: Distinguish between received and sent messages !!!
                message = self.q_messages.get(timeout=delay)
                # We don't so we send a dummy one
                print('generator: got a real message:', message)
            except Empty:
                print('generator: sending a dummy message')
                buddy = Buddy.get(alias='Carol')
                length = int(gauss(10, 8))
                self.adapter.send_im_msg('?DUMMY:' + ('.' * max(1, length)),
                                         buddy.identifier)
