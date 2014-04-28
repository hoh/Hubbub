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

import drugstore.stats as stats

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
            lib.js('/stats/obfuscated_profile_outgoing.js'),
            lib.js('/stats/real_profile.js'),
            lib.js('/stats/real_profile_outgoing.js'),
        ),
        t.body(
            t.h1('Statistics'),

            t.h2('Total traffic'),
            t.div(id='sent_vs_recv'),

            t.h2('Messages per minute'),
            t.div(id='sent_and_recv_over_time'),

            t.h2('Obfuscated outgoing profile'),
            t.div(id='obfuscated_profile_outgoing'),

            t.h2('Real outgoing profile'),
            t.div(id='real_profile_outgoing'),

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
            var x = chart.addCategoryAxis("x", "Direction");
            var y = chart.addMeasureAxis("y", "Count");
            chart.addSeries("Type", dimple.plot.bar);
            chart.assignColor("Real", "#95A5E0");
            chart.assignColor("Dummy", "#DA9694");
            chart.addLegend(180, 10, 360, 20, "right");
            chart.draw();

            y.titleShape.text("Message Count");
        })
        '''


@app.route('/stats/sent_vs_recv.json')
def sent_vs_recv_json():
    return json.dumps(stats.sent_vs_recv())


@app.route('/stats/sent_and_recv_over_time.js')
def sent_and_recv_over_time_js():
    return '''
        var sent_and_recv_over_time = dimple.newSvg("#sent_and_recv_over_time", 800, 400);
        d3.json("/stats/sent_and_recv_over_time.json", function (data) {
            var chart = new dimple.chart(sent_and_recv_over_time, data);
            var x = chart.addCategoryAxis("x", "Date");
            x.addOrderRule("Date");
            var y = chart.addMeasureAxis("y", "Count");
            chart.addSeries("Direction", dimple.plot.bar);
            chart.assignColor("Real", "#95A5E0");
            chart.assignColor("Dummy", "#DA9694");
            chart.addLegend(180, 10, 360, 20, "right");
            chart.draw();

            y.titleShape.text("Message Count");
        })
        '''


@app.route('/stats/sent_and_recv_over_time.json')
def sent_and_recv_over_time_json():
    return json.dumps(stats.sent_and_recv_over_time())


@app.route('/stats/obfuscated_profile.js')
def obfuscated_profile_js():
    return '''
        var obfuscated_profile = dimple.newSvg("#obfuscated_profile", 800, 400);
        d3.json("/stats/obfuscated_profile.json", function (data) {
            var chart = new dimple.chart(obfuscated_profile, data);
            var x = chart.addCategoryAxis("x", ["Buddy", "Direction"]);
            var y = chart.addMeasureAxis("y", "Count");
            chart.addSeries("Type", dimple.plot.bar);
            chart.assignColor("Real", "#95A5E0");
            chart.assignColor("Dummy", "#DA9694");
            chart.addLegend(200, 10, 380, 20, "right");
            chart.draw();

            x.titleShape.text("Contact / Sent vs Received");
            y.titleShape.text("Message Count");
        })
    '''

@app.route('/stats/obfuscated_profile.json')
def obfuscated_profile_json():
    return json.dumps(stats.obfuscated_profile())


@app.route('/stats/obfuscated_profile_outgoing.js')
def obfuscated_profile_outgoing_js():
    return '''
        var obfuscated_profile_outgoing = dimple.newSvg("#obfuscated_profile_outgoing", 800, 400);
        d3.json("/stats/obfuscated_profile_outgoing.json", function (data) {
            var chart = new dimple.chart(obfuscated_profile_outgoing, data);
            var x = chart.addCategoryAxis("x", ["Buddy"]);
            var y = chart.addMeasureAxis("y", "Count");
            chart.addSeries("Type", dimple.plot.bar);
            chart.assignColor("Real", "#95A5E0");
            chart.assignColor("Dummy", "#DA9694");
            chart.addLegend(200, 10, 380, 20, "right");
            //chart.noFormats = true;
            chart.draw();

            x.titleShape.text("Contact");
            y.titleShape.text("Message Count");
        })
    '''


@app.route('/stats/obfuscated_profile_outgoing.json')
def obfuscated_profile_outgoing_json():
    return json.dumps(stats.obfuscated_profile_outgoing())


@app.route('/stats/real_profile.js')
def real_profile_js():
    return '''
        var real_profile = dimple.newSvg("#real_profile", 800, 400);
        d3.json("/stats/real_profile.json", function (data) {
            var chart = new dimple.chart(real_profile, data);
            var x = chart.addCategoryAxis("x", ["Buddy", "Direction"]);
            var y = chart.addMeasureAxis("y", "Count");
            chart.addSeries("Type", dimple.plot.bar);
            chart.assignColor("Real", "#95A5E0");
            chart.assignColor("Dummy", "#DA9694");
            chart.addLegend(200, 10, 380, 20, "right");
            chart.draw();

            x.titleShape.text("Contact / Sent vs Received");
            y.titleShape.text("Message Count");
        })
    '''


@app.route('/stats/real_profile.json')
def real_profile_json():
    return json.dumps(stats.real_profile())


@app.route('/stats/real_profile_outgoing.js')
def real_profile_outgoing_js():
    return '''
        var real_profile_outgoing = dimple.newSvg("#real_profile_outgoing", 800, 400);
        d3.json("/stats/real_profile_outgoing.json", function (data) {
            var chart = new dimple.chart(real_profile_outgoing, data);
            var x = chart.addCategoryAxis("x", ["Buddy"]);
            var y = chart.addMeasureAxis("y", "Count");
            chart.addSeries("Type", dimple.plot.bar);
            chart.assignColor("Real", "#95A5E0");
            chart.assignColor("Dummy", "#DA9694");
            chart.addLegend(200, 10, 380, 20, "right");
            chart.draw();

            x.titleShape.text("Contact");
            y.titleShape.text("Message Count");
        })
    '''


@app.route('/stats/real_profile_outgoing.json')
def real_profile_outgoing_json():
    return json.dumps(stats.real_profile_outgoing())
