from scapy.all import *
from deep_translator import GoogleTranslator
from pprint import pprint
import time
import io
import os
import magic
import pprint
import pyshark
import json


global rm
rm=False

conf.dot15d4_protocol = "sixlowpan"
yandex = GoogleTranslator(source='zh-TW', target='en')

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def remove():
    if rm:
        rm=False
        os.system('echo > '+ ROOT_DIR + "/wpan.pcap")
        return False
    return True

def translate(line):
    res=line.decode('utf-16be', 'ignore').lower()
    res=re.sub('([^\u0020-\u007E]+)', ' \g<1> ', res)
    res=re.sub('\s{2,}', '', res)
    print('x'*35)
    time.sleep(0.6)
    #print(res)
    res=str(yandex.translate(res))
    res=re.sub('é|è|ê', 'e', res)
    res=re.sub('â|à', 'a', res)
    res=re.sub('ô|ö', 'o', res)
    res=re.sub('î|ï', 'i', res)
    res=re.sub('û|ü', 'u', res)
    res=res.encode('utf-16be', 'ignore')
    res=str(res.decode('utf-8', 'ignore'))

    print(res)
    hexdump(line.decode('utf-8', 'ignore')+res)

mime = magic.Magic(mime=True)
while 1:
    try:
        pkts=rdpcap(ROOT_DIR + "/wpan.pcap")
        for p in pkts:
            print(p.summary())
            if p:
                if (p.payload and len(p.payload.payload)):
                    print('='*35)
                    pkt_payload = bytes(p.payload.payload)
                    stype=mime.from_buffer(pkt_payload)
                    print(stype)
                    translate(pkt_payload)
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
            os.system('touch ' + ROOT_DIR + "/wpan.pcap")
        print(e)
        #remove(rm)
        pass