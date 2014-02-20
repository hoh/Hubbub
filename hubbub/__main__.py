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

from multiprocessing import Process


def run_adapter():
    print('run_adapter')
    from adapter import PidginDBusAdapter

    adapter = PidginDBusAdapter()
    adapter.run()


def run_bottle():
    print('run_bottle')
    from webui import app

    app.run(debug=True, reload=True)


def run_generator():
    print('run_generator')
    from generator import HeartBeatGenerator
    from adapter import PidginDBusAdapter

    adapter = PidginDBusAdapter()
    generator = HeartBeatGenerator(adapter)
    generator.run()

if __name__ == '__main__':

    wait_for_process = None

    if 'pidgin' in sys.argv:
        pa = Process(target=run_adapter)
        pa.start()
        wait_for_process = pa

    if 'setup' in sys.argv:
        from drugstore.models import create as create_db
        create_db()

    if 'webui' in sys.argv:
        pb = Process(target=run_bottle)
        pb.start()
        wait_for_process = pb

    if 'generator' in sys.argv:
        pc = Process(target=run_generator)
        pc.start()
        wait_for_process = pc

    if wait_for_process:
        wait_for_process.join()
