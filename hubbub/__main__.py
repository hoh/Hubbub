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

from multiprocessing import Process
from adapter import PidginDBusAdapter


def run_adapter(adapter_class):
    print('run_adapter')
    adapter = adapter_class()
    adapter.run()


def run_bottle(adapter_class):
    print('run_bottle')
    adapter = adapter_class()
    from bottle import Bottle
    app = Bottle()

    @app.route('/send')
    def send():
        adapter.send_im_msg('?DUMMY:bottle')

    app.run(debug=True, reload=True)

if __name__ == '__main__':
    adapter_class = PidginDBusAdapter

    pa = Process(target=run_adapter, args=(adapter_class,))
    pa.start()
    # pa.join()
    pb = Process(target=run_bottle, args=(adapter_class,))
    pb.start()
    pb.join()
