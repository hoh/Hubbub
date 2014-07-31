#!/bin/bash
sudo rm -r ubuntu/usr

sudo mkdir -p ubuntu/usr/lib/python3/dist-packages/

sudo cp -r ../hubbub ubuntu/usr/lib/python3/dist-packages/hubbub
sudo rm -r `find ubuntu/usr/ | grep "__pycache__$"`
sudo rm -r `find ubuntu/usr/ | grep "\.pyc$"`
sudo find ubuntu/usr/ -type d -exec chmod 755 {} \;
sudo find ubuntu/usr/ -type f -exec chmod 644 {} \;
sudo chown -R root ubuntu/usr
sudo chgrp -R root ubuntu/usr

dpkg --build ubuntu
echo "ready to test ?"
read
lintian ubuntu.deb

mv ubuntu.deb hubbub_0.1-1_amd64.deb

echo "moving to VM"
sudo cp hubbub_0.1-1_amd64.deb /home/okso/.local/share/lxc/hubbub-build2/rootfs/home/ubuntu/hubbub_0.1-1_amd64.deb

