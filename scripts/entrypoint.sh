

set -e

base="/opt/gr-wban/base.pcap"
file="/opt/gr-wban/new.pcap"
file_type="/opt/gr-wban/type.bin"
header="/opt/gr-wban/header.bin"
translate="/opt/gr-wban/ts.bin"

make_fifo () {
    [[ ! -f $1 ]] && rm -rvf $1 && mkfifo $1 || mkfifo $1
}

main () {
    gnuradio-companion /opt/gr-wban/*.grc &>/dev/null &
    python3 readPcap.py
}
main

