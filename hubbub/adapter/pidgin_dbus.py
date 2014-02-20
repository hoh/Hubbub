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


import dbus
import time

from gi.repository import GObject
from dbus.mainloop.glib import DBusGMainLoop

DBusGMainLoop(set_as_default=True)

from drugstore import store


class PidginDBusAdapter:
    output = None

    def __init__(self):

        bus = dbus.SessionBus()

        # --- Callbacks:

        bus.add_signal_receiver(
            self.received_im_msg,
            dbus_interface="im.pidgin.purple.PurpleInterface",
            signal_name="ReceivedImMsg")

        bus.add_signal_receiver(
            self.receiving_im_msg,
            dbus_interface="im.pidgin.purple.PurpleInterface",
            signal_name="ReceivingImMsg")

        bus.add_signal_receiver(
            self.sending_im_msg,
            dbus_interface="im.pidgin.purple.PurpleInterface",
            signal_name="SendingImMsg")

        bus.add_signal_receiver(
            self.sent_im_msg,
            dbus_interface="im.pidgin.purple.PurpleInterface",
            signal_name="SentImMsg")

        bus.add_signal_receiver(
            self.writing_im_msg,
            dbus_interface="im.pidgin.purple.PurpleInterface",
            signal_name="WritingImMsg")

        bus.add_signal_receiver(
            self.wrote_im_msg,
            dbus_interface="im.pidgin.purple.PurpleInterface",
            signal_name="WroteImMsg")

        # --- Setup to send messages:

        obj = bus.get_object(
            "im.pidgin.purple.PurpleService",
            "/im/pidgin/purple/PurpleObject")

        self.purple = dbus.Interface(
            obj,
            "im.pidgin.purple.PurpleInterface")

    def run(self):
        loop = GObject.MainLoop()
        loop.run()

    def received_im_msg(self, account, sender, message, conversation, flags):
        'Receives user incoming messages, after being filtered by plugins.'
        # print('received_im_msg', account, sender, message, conversation, flags)
        pass

    def receiving_im_msg(self, account, sender, message, conversation, flags):
        'Receives all incoming messages, including dummies.'
        # print('receiving_im_msg', account, sender, message, conversation, flags)
        pass

    def sending_im_msg(self, *args):
        # print('sending_im_msg', args)
        pass

    def sent_im_msg(self, *args):
        # print('sent_im_msg', args)
        pass

    def wrote_im_msg(self, account, sender, message, conversation, flags):
        # record('wrote_im_msg', message)
        # print('wrote_im_msg', args)
        pass

    # def writing_im_msg(self, *args):
    def writing_im_msg(self, account, sender, message, conversation, flags):
        print('writing_im_msg', account, sender, message, conversation, flags)
        if '/' in sender:
            buddy, buddy_device = sender.split('/')
        else:
            buddy, buddy_device = sender, None

        if flags == 1:
            print('You sent', message)
            store(message, buddy=buddy, received=False)
        else:
            print('You received', message, 'from', sender)
            store(message, buddy=buddy, received=True)

    def send_im_msg(self, message):
        print('send_im_msg', message)
        for conv in self.purple.PurpleGetIms():
            print(' -conv', conv)
            self.purple.PurpleConvImSend(
                self.purple.PurpleConvIm(conv),
                message)
