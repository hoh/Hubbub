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

from multiprocessing import Queue


def do_fork():
    "Forking as a daemon"
    if os.fork():
        sys.exit()
    else:
        # Wait for Pidgin to setup DBus etc
        time.sleep(2)


def run_adapter(q_messages):
    print('run_adapter')
    from hubbub.adapter.pidgin_dbus import PidginDBusAdapter

    adapter = PidginDBusAdapter(q_messages)
    adapter.run()


def run_update_contacts():
    "Updating contacts database every n seconds"
    from hubbub.adapter.pidgin_dbus import PidginDBusAdapter
    adapter = PidginDBusAdapter(None)
    while True:
        adapter.update_contacts()
        time.sleep(30)


def run_generators(q_messages, fake=False):
    print('run_generator')
    from hubbub.generator import HeartBeatGenerator

    if fake:
        from hubbub.adapter.fake import FakeAdapter as Adapter
    else:
        from hubbub.adapter.pidgin_dbus import PidginDBusAdapter as Adapter
    adapter = Adapter(None)  # Write-only adapter, no queue

    import threading
    try:  # Py2
        from Queue import Queue as QQueue
    except ImportError:  # Py3
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