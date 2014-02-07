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

'''
Web User Interface for Hubbub, built using Tumulus.
'''

import json

from tumulus.tags import HTMLTags as t
import tumulus.lib as lib

from .bottle import Bottle

from drugstore.stats import sent_vs_recv

app = application = Bottle()


@app.route('/')
def index():
    return t.html(
        t.head(
            lib.js('d3'),
            lib.js('dimple'),
            lib.js('/graph.js'),
        ),
        t.body(
            t.h1('Statistics'),
            t.div(id='graph'),
        ),
    ).build()


@app.route('/graph.js')
def graph():
    return '''
        var svg = dimple.newSvg("#graph", 800, 400);
        d3.json("/data.json", function (data) {
            var chart = new dimple.chart(svg, data);
            chart.addCategoryAxis("x", "Direction");
            chart.addMeasureAxis("y", "Count");
            chart.addSeries("Type", dimple.plot.bar);
            chart.draw();
        })
        '''


@app.route('/data.json')
def data():
    return json.dumps(sent_vs_recv())
