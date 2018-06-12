#!/bin/env sh

sudo apt-get update
sudo apt-get -y install check
# alternatively git clone git@gitlab.com:gnutls/libtasn1.git
sudo apt-get -y install libtasn1-6-dev libtasn1-bin
git clone https://github.com/jadeblaquiere/ecclib.git
cd ecclib
autoreconf --install
./configure --prefix=/usr
make
sudo make install
sudo pip3 install --upgrade .
cd ..
