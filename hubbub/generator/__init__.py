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

from random import random
from time import sleep
from multiprocessing import Queue


class HeartBeatGenerator(object):
    '''
        Generates new messages at relatively constant time intervals.
        (relatively = random around an average)
    '''
    period = 10  # average period between messages, in seconds

    def __init__(self, adapter, q_messages):
        self.adapter = adapter
        self.q_messages = q_messages

    def run(self):
        while True:
            delay = random() * self.period * 2
            try:
                # We get a real message
                # TODO: Distinguish between received and sent messages !!!
                message = q_messages.get(timeout=delay)
                # We don't so we send a dummy one
            except Queue.Empty:
                self.adapter.send_im_msg('?DUMMY:fixed_size', 'carol@okso.me')
