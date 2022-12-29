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
    ls
}
adaptkarel () {
    cd /opt
    git clone https://github.com/karel/gr-adapt
    cd gr-adapt
    mkdir build
    cd build
    cmake ../
    make -j$(nproc)
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

## Local
calcWeigth () {
    git clone https://github.com/Maissacrement/CalculWeigthBetweenTwoHexString.git
    cd CalculWeigthBetweenTwoHexString
    mkdir build
    cd build
    cmake ..
    make
    ls
    cp ./calcWeight.cpython-38-x86_64-linux-gnu.so /usr/local/lib/python3.8/dist-packages/
    ldconfig
}

main () {
    adaptkarel
    osmosdr
    gr_ieee_802_15_4
    rf_tap
    foo
    calcWeigth
}

main