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


class HeartBeatGenerator(object):
    '''
        Generates new messages at relatively constant time intervals.
        (relatively = random around an average)
    '''
    period = 10  # average period between messages, in seconds

    def __init__(self, adapter):
        self.adapter = adapter

    def run(self):
        while True:
            self.adapter.send_im_msg('?DUMMY:fixed_size', 'carol@okso.me')
            sleep(random() * self.period * 2)
