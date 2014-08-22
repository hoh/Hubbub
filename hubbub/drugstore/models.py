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

import os.path
from .peewee import (
    Model, SqliteDatabase,
    CharField, DateTimeField, BooleanField, IntegerField,
)

SETTINGS_PATH = os.path.expanduser("~/.hubbub/")
if not os.path.isdir(SETTINGS_PATH):
    os.makedirs(SETTINGS_PATH)
DB_PATH = SETTINGS_PATH + "hubbub.db"

db = SqliteDatabase(DB_PATH, threadlocals=True)


class Message(Model):
    length = IntegerField()
    date = DateTimeField()
    dummy = BooleanField()
    received = BooleanField()
    buddy = CharField()

    class Meta:
        database = db


class Buddy(Model):
    account = IntegerField(null=True)
    identifier = CharField()
    alias = CharField()
    enabled = BooleanField(default=False)

    def __unicode__(self):
        return '{} ({}) {}'.format(
            self.alias,
            self.identifier,
            '(disabled)' * (not self.enabled))

    class Meta:
        database = db


def create():
    db.create_tables([Message, Buddy], True)
    #for model in Message, Buddy:
    #    try:
    #        model.create_table()
    #    except OperationalError as error:
    #        continue
            #if "already exists" in error.args[0]:
            #    print("Table already exists:", model)
            #    continue
            #else:
            #    raise error

    #Buddy(identifier='carol@okso.me', alias='Carol').save()
    #Buddy(identifier='dan@okso.me', alias='Dan').save()
