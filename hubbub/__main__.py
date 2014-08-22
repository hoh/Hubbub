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

from multiprocessing import Process, Queue

USAGE = '''
NAME
    hubbub
SYNOPSIS
    hubbub [setup] [pidgin] [generator] [webui] [contacts] [simulator]
OPTIONS
    Default: contacts pidgin generator webui

    nosetup
        Do not create a new SQLite database even if none exists.
    contacts
        Imports your Pidgin contacts into Hubbub
    pidgin
        Connect to Pidgin via DBus to collect a copy of the user's traffic.
    generator
        Generate dummy messages and send them through Pidgin via DBus.
        (fake): Local tests without sending dummy messages to Pidgin.
    webui
        Launch a web user interface on http://localhost:8080 to monitor the
        actions of Hubbub.
    simulator
        Run a simulation instead.
'''


def run_adapter(q_messages):
    print('run_adapter')
    from hubbub.adapter.pidgin_dbus import PidginDBusAdapter

    adapter = PidginDBusAdapter(q_messages)
    adapter.run()


def run_bottle(q_messages=None):
    print('run_bottle')
    from hubbub.webui import app
    app.q_messages = q_messages
    app.run(host='localhost', port=8900, debug=True, reload=True)


def run_update_contacts():
    "Updating contacts database every n seconds"
    from hubbub.adapter.pidgin_dbus import PidginDBusAdapter
    adapter = PidginDBusAdapter(None)
    while True:
        adapter.update_contacts()
        time.sleep(30)


def run_generators(q_messages):
    print('run_generator')
    from hubbub.generator import HeartBeatGenerator

    if 'fake' in argv:
        from hubbub.adapter.fake import FakeAdapter as Adapter
    else:
        from hubbub.adapter.pidgin_dbus import PidginDBusAdapter as Adapter
    adapter = Adapter(None)  # Write-only adapter, no queue

    import threading
    try:
        from Queue import Queue as QQueue
    except ImportError:
        from queue import Queue as QQueue
    def start_generator(buddy, q):
        print('B', [buddy.id])
        generator = HeartBeatGenerator(adapter, buddy.id, q)
        generator.run()

    from hubbub.drugstore.models import Buddy
    queues = {}
    #for buddy in Buddy.select().where(Buddy.enabled):
    for buddy in Buddy.select():
        q = QQueue()
        queues[buddy.identifier] = q
        t = threading.Thread(target=start_generator, args=(buddy, q))
        t.start()

    while True:
        msg = q_messages.get()
        for q in queues.values():
            q.put(msg)


def run_simulator():
    print('run_simulator')
    from hubbub.generator.generator import Simulator
    from hubbub.generator.heartbeat import HeartBeatSimulator
    from hubbub.datasets.simulations import SIMPLE_LOG
    # simulator = Simulator(SIMPLE_LOG)
    simulator = HeartBeatSimulator(SIMPLE_LOG)
    result = simulator.run()
    assert result


if __name__ == '__main__':

    # Forking as a daemon:
    if 'fork' in sys.argv:
        if os.fork():
            sys.exit()
        else:
            # Wait for Pidgin to setup DBus etc
            time.sleep(2)

    argv = sys.argv[1:]
    if not argv or argv == ['fork']:  # default
        argv = ['contacts', 'pidgin', 'generator', 'webui']

        wait_for_process = None
    # Queue in which observed messages will be pushed
    # for the generator to take into account.
    q_messages = Queue()

    if not 'nosetup' in argv:
        from hubbub.drugstore.models import create as create_db
        create_db()

    if 'contacts' in argv:
        pe = Process(target=run_update_contacts)
        pe.start()
        wait_for_process = pe

    if 'pidgin' in argv:
        pa = Process(target=run_adapter, args=(q_messages,))
        pa.start()
        wait_for_process = pa

    if 'generator' in argv:
        pc = Process(target=run_generators, args=(q_messages,))
        pc.start()
        wait_for_process = pc

    if 'simulator' in argv:
        pd = Process(target=run_simulator)
        pd.start()
        wait_for_process = pd

    if 'webui' in argv:
        pb = Process(target=run_bottle, args=(q_messages,))
        pb.start()
        wait_for_process = pb

    if 'testqueue' in argv:
        # For tests only, delete this afterwards, consumption
        # should go in the generator.
        print('Queing...')
        while True:
            print('Pop', q_messages.get())

    if wait_for_process:
        wait_for_process.join()
    elif 'setup' not in argv:
        print(USAGE)
