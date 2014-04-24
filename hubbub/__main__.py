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

import sys

from multiprocessing import Process, Queue

USAGE = '''
NAME
    hubbub
SYNOPSIS
    hubbub [setup] [pidgin] [generator] [webui]
OPTIONS
    setup
        Creates a new SQLite database to keep track of metadata for learning.
    pidgin
        Connect to Pidgin via DBus to collect a copy of the user's traffic.
    generator
        Generate dummy messages and send them through Pidgin via DBus.
    webui
        Launch a web user interface on http://localhost:8080 to monitor the
        actions of Hubbub.
'''


def run_adapter(q_messages):
    print('run_adapter')
    from adapter.pidgin_dbus import PidginDBusAdapter

    adapter = PidginDBusAdapter(q_messages)
    adapter.run()


def run_bottle():
    print('run_bottle')
    from webui import app

    app.run(debug=True, reload=True)


def run_generator(q_messages):
    print('run_generator')
    from generator import HeartBeatGenerator

    if 'fake' in sys.argv:
        from adapter.fake import FakeAdapter as Adapter
    else:
        from adapter.pidgin_dbus import PidginDBusAdapter as Adapter

    adapter = Adapter(None)  # Write-only adapter, no queue
    generator = HeartBeatGenerator(adapter, q_messages)
    generator.run()

if __name__ == '__main__':

    wait_for_process = None
    # Queue in which observed messages will be pushed
    # for the generator to take into account.
    q_messages = Queue()

    if 'setup' in sys.argv:
        from drugstore.models import create as create_db
        create_db()

    if 'pidgin' in sys.argv:
        pa = Process(target=run_adapter, args=(q_messages,))
        pa.start()
        wait_for_process = pa

    if 'generator' in sys.argv:
        pc = Process(target=run_generator, args=(q_messages,))
        pc.start()
        wait_for_process = pc

    if 'webui' in sys.argv:
        pb = Process(target=run_bottle)
        pb.start()
        wait_for_process = pb

    if 'testqueue' in sys.argv:
        # For tests only, delete this afterwards, consumption
        # should go in the generator.
        print('Queing...')
        while True:
            print('Pop', q_messages.get())

    if wait_for_process:
        wait_for_process.join()
    elif 'setup' not in sys.argv:
        print(USAGE)
