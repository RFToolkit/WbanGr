#!/bin/sh

osmosdr () {
    cd /opt
    git clone git://git.osmocom.org/gr-osmosdr
    cd gr-osmosdr/
    mkdir build
    cd build/
    cmake ../
    make
    make install
    ldconfig
}

main () {
    osmosdr
}

main