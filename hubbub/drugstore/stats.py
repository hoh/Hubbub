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

from .models import Message


def sent_vs_recv():
    msg_all = Message.select()

    return [{"Direction": "Received" if received else "Sent",
             "Type": "Dummy" if dummy else "Real",
             "Count": (
                 msg_all
                 .where(Message.received == received)
                 .where(Message.dummy == dummy)
                 .count()
                 ),
             }
            for received in (True, False)
            for dummy in (True, False)
            ]


def sent_and_recv_over_time():
    msg_all = Message.select().where(Message.dummy == False)

    return [{"Direction": "Received" if msg.received else "Sent",
             "Type": "Real",
             "Date": msg.date.strftime('%Y-%m-%dT%H:%M'),  # Minute, no seconds
             "Count": 1,
             }
            for msg in msg_all
            ]


def obfuscated_profile():
    buddies = tuple(m.buddy for m in Message.select(Message.buddy).distinct())

    return [{
        'Type': 'Dummy' if dummy else 'Real',
        'Direction': 'Received' if received else 'Sent',
        'Buddy': buddy,
        'Count': Message.select().where(
            Message.dummy == dummy,
            Message.received == received,
            Message.buddy == buddy,
            ).count()
        }
        for received in (True, False)
        for dummy in (True, False)
        for buddy in buddies
    ]


def obfuscated_profile_outgoing():
    buddies = tuple(m.buddy for m in Message.select(Message.buddy).distinct())

    return [{
        'Type': 'Dummy' if dummy else 'Real',
        'Buddy': buddy,
        'Count': Message.select().where(
            Message.dummy == dummy,
            Message.received == False,
            Message.buddy == buddy,
            ).count()
        }
        for dummy in (True, False)
        for buddy in buddies
    ]


def real_profile():
    buddies = tuple(m.buddy for m in Message.select(Message.buddy).distinct())

    return [{
        'Type': 'Real',
        'Direction': 'Received' if received else 'Sent',
        'Buddy': buddy,
        'Count': Message.select().where(
            Message.dummy == False,
            Message.received == received,
            Message.buddy == buddy,
            ).count()
        }
        for received in (True, False)
        for buddy in buddies
    ]


def real_profile_outgoing():
    buddies = tuple(m.buddy for m in Message.select(Message.buddy).distinct())

    return [{
        'Type': 'Real',
        'Buddy': buddy,
        'Count': Message.select().where(
            Message.dummy == False,
            Message.received == False,
            Message.buddy == buddy,
            ).count()
        }
        for buddy in buddies
    ]
