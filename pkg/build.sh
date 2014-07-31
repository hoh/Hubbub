#!/bin/bash

sudo rm -r ubuntu/usr

sudo mkdir -p ubuntu/usr/lib/python3/dist-packages/
sudo mkdir -p ubuntu/usr/lib/pidgin/

sudo cp -r ../hubbub ubuntu/usr/lib/python3/dist-packages/hubbub
sudo cp ../../Hubbub-Pidgin/pidgin-2.10.9/libpurple/plugins/hubbub-pidgin.so ubuntu/usr/lib/pidgin/hubbub-pidgin.so
sudo rm -r `find ubuntu/usr/ | grep "__pycache__$"`
sudo rm -r `find ubuntu/usr/ | grep "\.pyc$"`
sudo find ubuntu/usr/ -type d -exec chmod 755 {} \;
sudo find ubuntu/usr/ -type f -exec chmod 644 {} \;
sudo chown -R root ubuntu/usr
sudo chgrp -R root ubuntu/usr

dpkg --build ubuntu hubbub_0.1-1_`uname -m`.deb
echo "ready to test ?"
read
lintian hubbub_0.1-1_`uname -m`.deb

echo "moving to VM"
sudo cp hubbub_0.1-1_`uname -m`.deb /home/okso/.local/share/lxc/hubbub-build2/rootfs/home/ubuntu/hubbub_0.1-1_`uname -m`.deb

cp hubbub_0.1-1_`uname -m`.deb $HOME/web/hubbub_`uname -m`.deb
