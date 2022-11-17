from scapy.all import *
from deep_translator import GoogleTranslator
import time
import io
import os
import magic
import pprint
import pyshark


global rm
rm=False

conf.dot15d4_protocol = "sixlowpan"
yandex = GoogleTranslator(source='zh-TW', target='fr')

def remove():
    if rm:
        rm=False
        os.system('echo > /tmp/in.pcap')
        return False
    return True

def translate(line):
    res=line.decode('big5', 'ignore')
    res=re.sub('([^\u0020-\u007E]+)', ' \g<1> ', res)
    res=re.sub('\s+', ' ', res)
    print('x'*35)
    time.sleep(0.6)
    res=str(yandex.translate(res))
    res=re.sub('é|è|ê', 'e', res)
    res=re.sub('â|à', 'a', res)
    res=res.encode('gbk', 'ignore')
    res=res.decode('ascii', 'ignore')

    return res

mime = magic.Magic(mime=True)
while 1:
    try:
        pkts=rdpcap("/tmp/in.pcap")
        for p in pkts:
            print(p.summary())
            if p:
                if (p.payload and len(p.payload.payload)):
                    print('='*35)
                    pkt_payload = bytes(p.payload.payload)
                    stype=mime.from_buffer(pkt_payload)
                    print(stype)
                    print(translate(pkt_payload))
                    print('='*35)
        rm=True
        remove()
        time.sleep(1)
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
    except Exception as e:
        if "Not a supported capture file" in str(e):
            rm=True
            remove()
        if "No such":
            os.system('touch /tmp/in.pcap')
        #remove(rm)
        pass