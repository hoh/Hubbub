#!/bin/bash

ssh vm0 "rm -r hubbub"
scp -pr hubbub vm0:
#scp load_dbus_ssh.sh vm0:/tmp/load_dbus_ssh.sh
#ssh vm0 "source /tmp/load_dbus_ssh.sh ; python3 hubbub"
