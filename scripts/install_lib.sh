#!/bin/sh

osmosdr () {
    cd /opt
    git clone --recursive git://git.osmocom.org/gr-osmosdr
    cd gr-osmosdr/
    mkdir build
    cd build/
    cmake ../
    make
    make install
    ldconfig
}

gr_ieee_802_15_4 () {
    cd /opt
    git clone https://github.com/bastibl/gr-ieee802-15-4.git
    cd gr-ieee802-15-4/
    mkdir build
    cd build/
    cmake ../
    make
    make install
    ldconfig
}

rf_tap () {
    cd /opt
    git clone https://github.com/rftap/gr-rftap
    cd gr-rftap
    mkdir build
    cd build
    cmake ..
    make
    make install
    ldconfig
}

foo () {
    git clone https://github.com/bastibl/gr-foo.git
    cd gr-foo
    mkdir build
    cd build
    cmake ..
    make
    make install
    ldconfig
}

main () {
    osmosdr
    gr_ieee_802_15_4
    rf_tap
    foo
}

main