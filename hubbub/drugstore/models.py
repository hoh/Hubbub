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

from .peewee import (
    Model, SqliteDatabase,
    CharField, DateTimeField, BooleanField, IntegerField
)

db = SqliteDatabase('drugstore.db')


class Message(Model):
    text = CharField()
    length = IntegerField()
    date = DateTimeField()
    dummy = BooleanField()
    received = BooleanField()
    buddy = CharField()

    class Meta:
        database = db


class Buddy(Model):
    identifier = CharField()
    alias = CharField()
    enabled = BooleanField(default=True)

    def __unicode__(self):
        return '{} ({}) {}'.format(
            self.alias,
            self.identifier,
            '(disabled)' * self.enabled)

    class Meta:
        database = db


def create():
    Message.create_table()
    Buddy.create_table()

    Buddy(identifier='carol@okso.me', alias='Carol').save()
    Buddy(identifier='dan@okso.me', alias='Dan').save()
