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

from datetime import datetime

from bs4 import BeautifulSoup
from hubbub.drugstore import store
from hubbub.drugstore.models import Message


def adium(path, buddy):
    soup = BeautifulSoup(open(path))
    for xml_message in soup.find_all('message'):
        text = xml_message.contents[0].renderContents()
        m = Message(
            text=text,
            length=len(text),
            date=datetime.strptime(
                xml_message['time'].split('+')[0],
                '%Y-%m-%dT%H:%M:%S'),
            dummy=False,
            received=xml_message['sender'] == buddy,
            buddy=buddy,
            )
        m.save()

if __name__ == '__main__':
    adium('/Users/okso/Documents/Thesis/Hubbub/learning_sets/Nomad/alice@okso.me (2014-02-07T14.01.02+0100).xml', 'alice@okso.me')
    adium('/Users/okso/Documents/Thesis/Hubbub/learning_sets/Nomad/-639737832@chat.facebook.com (2013-12-07T18.58.28+0100).xml', '-639737832@chat.facebook.com')
