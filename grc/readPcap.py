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
yandex = GoogleTranslator(source='zh-TW', target='en')

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def remove():
    if rm:
        rm=False
        os.system('echo > /tmp/in.pcap')
        return False
    return True

def translate(line):
    res=line.decode('gbk', 'ignore')
    res=re.sub('([^\u0020-\u007E]+)', ' \g<1> ', res)
    res=re.sub('\s+', ' ', res)
    print('x'*35)
    time.sleep(0.6)
    print(res)
    res=str(yandex.translate(res))
    res=re.sub('é|è|ê', 'e', res)
    res=re.sub('â|à', 'a', res)
    res=res.encode('gbk', 'ignore')
    res=res.decode('utf-8', 'ignore')

    print(res)
    hexdump(line.decode('utf-8', 'ignore')+res)

mime = magic.Magic(mime=True)
while 1:
    try:
        pkts=rdpcap(ROOT_DIR + "/wpan.pcap")
        import json
        from pprint import pprint
        """sessions = pkts.sessions()
        for session in sessions:
            http_payload = ""
            for packet in sessions[session]:
                try:
                    if packet[TCP].dport == 80 or packet[TCP].sport == 80:
                        print(packet[TCP].payload)
                except:
                    pass"""
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
        print(e)
        #remove(rm)
        pass