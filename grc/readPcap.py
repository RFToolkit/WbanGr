from scapy.all import *
from deep_translator import GoogleTranslator
from pprint import pprint
import time
import io
import os
import magic
import json

global rm
rm=False

conf.dot15d4_protocol = "sixlowpan"
yandex = GoogleTranslator(source='zh-TW', target='fr')

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

color=lambda x, c=bcolors.OKGREEN: c + str(x) + '\x1b[0m'

def remove():
    if rm:
        rm=False
        os.system('echo > '+ ROOT_DIR + "/wpan.pcap")
        return False
    return True

def translate(line):
    res=line.decode('gbk', 'ignore').lower()
    
    res=re.sub('([^\u0020-\u007E]+)', ' \g<1> ', res)
    res=re.sub('\s{2,}', '', res)
    print('x'*35)
    #time.sleep(0.6)
    #print(res)
    res=str(yandex.translate(res))
    res=re.sub('é|è|ê', 'e', res)
    res=re.sub('â|à', 'a', res)
    res=re.sub('ô|ö', 'o', res)
    res=re.sub('î|ï', 'i', res)
    res=re.sub('û|ü', 'u', res)
    res=res.encode('gbk', 'ignore')
    res=str(res.decode('utf-8', 'ignore'))

    #print(color(res))
    #print(color(line.decode('utf-8', 'ignore'), bcolors.OKCYAN))
    hexdump(line.decode('utf-8', 'ignore')+res)
    #hexdump(line)


from CalculWeigthBetweenTwoHexString.build .calcWeight import getMatchingCase
import struct
import dns.message

def rrdns(bdata):
    try:
        notify = dns.message.from_wire(bdata)
        print(color(notify))
        soa = notify.find_rrset(
            notify.answer, notify.question[0].name, dns.rdataclass.IN, dns.rdatatype.SOA
        )

        # Do something with the SOA RR here
        print("The serial number for", soa.name, "is", soa[0].serial)
    except:
        # No SOA RR in the answer section.
        pass

    return 0
        

mime = magic.Magic(mime=True)

while 1:
    try:
        pkts=rdpcap(ROOT_DIR + "/wpan.pcap")
        for pk in pkts:
            for p in pk:
                if p:
                    if (p.payload.payload and len(p.payload.payload)):
                        print(p.summary())
                        reversedBytes = bytes(p.payload.payload)
                        rrdns(reversedBytes)
                        print( getMatchingCase(str(reversedBytes.hex()[4:32+4]), ROOT_DIR+ "/id") )
                        reversedBytes = bytes([c for t in zip(reversedBytes[1::2], reversedBytes[::2]) for c in t])
                        #print(original)
                        #print('='*35)
                        pkt_payload = bytes(reversedBytes) + bytes('\n'.encode('gbk')) + bytes(p)
                        stype=mime.from_buffer(pkt_payload)
                        print(stype)
                        translate(pkt_payload)
                        #print('='*35)
        rm=True
        #remove()
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