

set -e

base="/opt/gr-wban/base.pcap"
file="/opt/gr-wban/new.pcap"
file_type="/opt/gr-wban/type.bin"
header="/opt/gr-wban/header.bin"
translate="/opt/gr-wban/ts.bin"

make_fifo () {
    [[ ! -f $1 ]] && rm -rvf $1 && mkfifo $1 || mkfifo $1
}

make_fifo ${base}
make_fifo ${file_type}
make_fifo ${file}
make_fifo ${header}
make_fifo ${translate}

stype () {
    echo \"\"\"$1\"\"\" 2>/dev/null | file - 2>/dev/null
}

async_func () {
    tshark -r ${file} -x | xxd -p -r >> ${base} &
    #cat ./base.pcap > ./file &
    #tail -f ${base} | xargs -0 -I{} stype "{}" > ${file_type} &
    #tail -f ${base} | file - > ${file_type} &
    echo
}

make_zigbee () {
    async_func
    cat ${base} | python3 /opt/gr-wban/binfilter.py
}

main () {
    #async_func
    gnuradio-companion /opt/gr-wban/*.grc &>/dev/null &
    pip install dnspython
    python3 readPcap.py
    #while true; do    tshark -r ${file} -d tcp.port==80,http -w - > /tmp/in.pcap; done &
    #tail -f ${file} | tshark -r - -w - >> /tmp/in.pcap &
    #sleep 30
    #tail -f ${base} | od -Ax -tx1 | text2pcap -i4 -m2000 - - 2>/dev/null | tshark -r - -x | xxd -p -r >> ${base} &
    #make_zigbee
    #gnuradio-companion /opt/gr-wban/*.grc
    #pip install python-magic deep-translator scapy
    #apt install bc
    #tail -f ${file} | xxd -p | grep --color=auto -Ei -f /opt/gr-wban/res.txt -o
    #tail -f python3 /opt/gr-wban/binfilter.py #| grep --color=auto -Eia -f /opt/gr-wban/dict2.txt
    #tail -f ${file} | xxd -p | grep --color=auto -Ei -f /opt/gr-wban/key2
    #tail -f /dev/null
    #python3 /opt/gr-wban/xor.py ${file}
}
main
#| xxd -p | grep --color=auto -Eio -f /opt/gr-wban/key2 -f <(echo "ok|start|stop|idle|end")
#tail -f ${file} | xxd
#tshark -r ${file} -x | grep --color=auto -f <(echo "ok|start|stop|idle|end")
#| grep --color=auto -Ei -f /opt/gr-wban/k3 -f <(echo "ok|start|stop|idle|end")
# 
#| od -Ax -tx1 | text2pcap -m32 -i4 - - 2>/dev/null | nc -l 5555

