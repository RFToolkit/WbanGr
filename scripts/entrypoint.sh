

set -e

file="/opt/gr-wban/new.pcap"

[[ -f ${file} ]] && mkfifo ${file}
gnuradio-companion /opt/gr-wban/*.grc &>/dev/null &
tshark -x -r /opt/gr-wban/*.pcap