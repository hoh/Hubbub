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

import sys, os, time
from os.path import dirname, realpath
from multiprocessing import Process, Queue

from hubbub.webui import app
from hubbub.launchers import (
    do_fork,
    do_createdb,
    run_adapter,
    run_update_contacts,
    run_generators,
    run_simulator,
    )

HERE = dirname(realpath(__file__))
USAGE = open(HERE + '/manpage.txt').read()


class Controller:

    def __init__(self):
        pass

    def run(self, argv):

        if 'fork' in argv:
            do_fork()

        do_createdb()

        q_messages = Queue()
        processes = {}

        if 'contacts' in argv:
            processes['contacts'] = Process(target=run_update_contacts)
            processes['contacts'].start()

        if 'pidgin' in argv:
            processes['pidgin_logs'] = Process(target=run_adapter, args=(q_messages,))
            processes['pidgin_logs'].start()

        if 'generator' in argv:
            fake = 'fake' in argv
            processes['generator'] = Process(target=run_generators, args=(q_messages, fake))
            processes['generator'].start()

        self.processes = processes

        app.q_messages = q_messages
        app.controller = self
        app.run(host='localhost', port=8900, debug=True, reload=True)


if __name__ == '__main__':
    argv = sys.argv[1:]
    c = Controller()
    c.run(argv)
