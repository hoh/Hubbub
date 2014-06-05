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

from random import random, gauss
from Queue import Empty

from datetime import timedelta

from hubbub.drugstore.models import Buddy
from hubbub.generator.generator import Generator, Simulator


class HeartBeatGenerator(Generator):
    '''
        Generates new messages at relatively constant time intervals.
        (relatively = random around an average)
    '''
    period = 2  # average period between messages, in seconds

    def run(self):
        while True:
            print('generator: new loop')
            delay = random() * self.period * 2  # TODO: Add exponential delay
            try:
                # We get a real message
                # TODO: Distinguish between received and sent messages !!!
                message = self.q_messages.get(timeout=delay)
                # We don't so we send a dummy one
                print('generator: got a real message:', message)
            except Empty:
                print('generator: sending a dummy message')
                buddy = Buddy.get(alias='carol')
                length = int(gauss(10, 8))
                self.adapter.send_im_msg('?DUMMY:' + ('.' * max(1, length)),
                                         buddy.identifier)


class HeartBeatSimulator(Simulator):

    period = 5

    def delay(self):
        return self.period * (random() * 2)

    def run(self, delay=None):
        delay = delay or self.delay
        dummy_messages = []

        start, end = self.date_boundaries()

        t = start

        for real in self.real_messages:
            while t < real[0]:
                dummy_messages.append((t, 10))
                #t += timedelta(seconds=delay())
                #t += timedelta(seconds=delay() * random())
                t += timedelta(seconds=delay() * random() * random()**0.5)
            # We got a real message:
            t = real[0] + timedelta(seconds=delay())

        # Finishing the last day:
        while t < end:
            dummy_messages.append((t, 10))
            t += timedelta(seconds=delay())

        return dummy_messages
