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

from drugstore.stats import (
    sent_vs_recv, sent_and_recv_over_time, obfuscated_profile, real_profile)

app = application = Bottle()


@app.route('/')
def index():
    return t.html(
        t.head(
            lib.js('d3'),
            lib.js('dimple'),
            lib.js('/stats/sent_vs_recv.js'),
            lib.js('/stats/sent_and_recv_over_time.js'),
            lib.js('/stats/obfuscated_profile.js'),
            lib.js('/stats/real_profile.js'),
        ),
        t.body(
            t.h1('Statistics'),

            t.h2('Total traffic'),
            t.div(id='sent_vs_recv'),

            t.h2('Messages per minute'),
            t.div(id='sent_and_recv_over_time'),

            t.h2('Obfuscated profile'),
            t.div(id='obfuscated_profile'),

            t.h2('Real profile'),
            t.div(id='real_profile'),
        ),
    ).build()


@app.route('/stats/sent_vs_recv.js')
def sent_vs_recv_js():
    return '''
        var sent_vs_recv = dimple.newSvg("#sent_vs_recv", 800, 400);
        d3.json("/stats/sent_vs_recv.json", function (data) {
            var chart = new dimple.chart(sent_vs_recv, data);
            chart.addCategoryAxis("x", "Direction");
            chart.addMeasureAxis("y", "Count");
            chart.addSeries("Type", dimple.plot.bar);
            chart.addLegend(180, 10, 360, 20, "right");
            chart.draw();
        })
        '''


@app.route('/stats/sent_vs_recv.json')
def sent_vs_recv_json():
    return json.dumps(sent_vs_recv())


@app.route('/stats/sent_and_recv_over_time.js')
def sent_and_recv_over_time_js():
    return '''
        var sent_and_recv_over_time = dimple.newSvg("#sent_and_recv_over_time", 800, 400);
        d3.json("/stats/sent_and_recv_over_time.json", function (data) {
            var chart = new dimple.chart(sent_and_recv_over_time, data);
            var x = chart.addCategoryAxis("x", "Date");
            x.addOrderRule("Date");
            chart.addMeasureAxis("y", "Count");
            chart.addSeries("Direction", dimple.plot.bar);
            chart.addLegend(180, 10, 360, 20, "right");
            chart.draw();
        })
        '''


@app.route('/stats/sent_and_recv_over_time.json')
def sent_and_recv_over_time_json():
    return json.dumps(sent_and_recv_over_time())


@app.route('/stats/obfuscated_profile.js')
def obfuscated_profile_js():
    return '''
        var obfuscated_profile = dimple.newSvg("#obfuscated_profile", 800, 400);
        d3.json("/stats/obfuscated_profile.json", function (data) {
            var chart = new dimple.chart(obfuscated_profile, data);
            chart.addCategoryAxis("x", ["Buddy", "Direction"]);
            chart.addMeasureAxis("y", "Count");
            chart.addSeries("Type", dimple.plot.bar);
            chart.addLegend(200, 10, 380, 20, "right");
            chart.draw();
        })
    '''


@app.route('/stats/obfuscated_profile.json')
def obfuscated_profile_json():
    return json.dumps(obfuscated_profile())


@app.route('/stats/real_profile.js')
def real_profile_js():
    return '''
        var real_profile = dimple.newSvg("#real_profile", 800, 400);
        d3.json("/stats/real_profile.json", function (data) {
            var chart = new dimple.chart(real_profile, data);
            chart.addCategoryAxis("x", ["Buddy", "Direction"]);
            chart.addMeasureAxis("y", "Count");
            chart.addSeries("Type", dimple.plot.bar);
            chart.addLegend(200, 10, 380, 20, "right");
            chart.draw();
        })
    '''


@app.route('/stats/real_profile.json')
def real_profile_json():
    return json.dumps(real_profile())
