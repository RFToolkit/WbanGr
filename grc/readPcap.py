from scapy.all import *
from deep_translator import GoogleTranslator, MyMemoryTranslator
from pprint import pprint
import time
import io
import os
import magic
import json

from itertools import cycle
from pydub import AudioSegment
from pydub.playback import play
from scipy.io import wavfile
import numpy as np
import sys
import io
import chardet
from scapy.layers.dot15d4 import Dot15d4Data, Dot15d4Cmd
from flask_cors import CORS,cross_origin
from flask import Flask, Response, request, render_template
from calcW import tcp, getGUDID

import base64

mime = magic.Magic(mime=True)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    static_folder='web/static',
    template_folder='web'
)
CORS(app, support_credentials=True)

rm=False

conf.dot15d4_protocol = "sixlowpan"
yandex = GoogleTranslator(source='zh-CN', target='en')



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

def remove(rm):
    if rm:
        rm=False
        os.system('echo > '+ ROOT_DIR + "/wpan8.pcap")
        return False
    return True

def ascii(din):
    return 'abcdefghijklmnopqrstwxyz'

def execXOR(line, k1):
    return ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(str(line), cycle(str(k1)))).encode('latin-1', errors='replace').replace(b"?", b" ").decode('utf-8', 'ignore')

def encodingUnpack(line, hex):
    detection = chardet.detect(line)
    encoding = detection["encoding"]
    ids=''
    # Know plain text 
    line=tcp(line.hex())[0]
    line+=''.join(chr(ord(c) ^ ord(k)) for c, k in zip(str(line), cycle(str('0a00')))).encode('latin-1', errors='replace').replace(b"?", b" ").decode('utf-8', 'ignore')
    line=line.encode(encoding, 'ignore').replace(b'\x00', b'').decode("utf-16be", 'ignore')
    line=re.sub('([^\u0020-\u007E]{1})', '\g<1>', line)
    
    u=line
    tsTxt=yandex.translate(line)
    if len(tsTxt):

        line=tsTxt.encode('utf-16be', 'ignore').replace(b'\x00', b'').decode("utf-16", 'ignore')
        u+=line+"\n"
        tsTxt=yandex.translate(line)
        if len(tsTxt):
            line=tsTxt.encode('utf-16be', 'ignore').replace(b'\x00', b'').decode("utf-16", 'ignore')
            u+=line+"\n"
            tsTxt=yandex.translate(u)
            if len(tsTxt): 
                line=tsTxt.encode('utf-16be', 'ignore').replace(b'\x00', b'')
                tsTxt=line.decode('utf-8', 'ignore')
                line=line.decode('utf-16be', 'ignore')
                line=tsTxt+line
                line=line.replace(r'\s{2,}', '').strip()
            line=line.replace('ying', 'ti')

        if (line):
            line=GoogleTranslator(source='auto', target='fr').translate(line)
            # GUID
            ids=getGUDID(line.encode('utf-8', 'ignore').hex()[4:4+8])
            print(ids)
            line=re.sub('([^\u0020-\u007E]{1})', '', line)

        hexdump(ids+line)
        return ids+line
    return 0

def translate(line, res):
    try:
        line=encodingUnpack(line, "4c5430312d4c54303220302e3030")
        if(len(line)):
            res['payload']=line
            res['type']=stype=str(mime.from_buffer(line))
            yield res
        else:
            line=encodingUnpack(line, "4c5430322d4c54303320302e3030")
            if(len(line)):
                res['payload']=line
                res['type']=stype=str(mime.from_buffer(line))
                yield response
    except:
        pass

def readPktSync():
    try:
        pkts=rdpcap(ROOT_DIR + "/wpan.pcap")
        for pk in pkts:
            for p in pk:
                rm=False
                if p:
                    src,dst,panid=None, None, None
                    if Dot15d4FCS in p:
                        if Dot15d4Data in p:
                            src=p[Dot15d4Data].src_panid
                            dst=p[Dot15d4Data].dest_panid
                            if src != None: src=hex(int(src))
                            if dst != None: dst=hex(int(dst))
                        if Dot15d4Beacon in p:
                            panid = hex(int(p[Dot15d4Beacon].src_panid))
                                
                                
                                
                    
                    if (p.payload.payload and len(p.payload.payload)):
                        
                        reversedBytes = bytes(p.payload.payload)
                        stype=str(mime.from_buffer(reversedBytes))
                        res=translate(reversedBytes, {  "src": src, "dst": dst, "panid": panid })
                        for edt in res:
                            yield json.dumps(edt)
    
    finally:
        print("End")

@app.route("/getpkt")
def hello_world():
    print('in')
    return Response(readPktSync(), mimetype="application/json")

@app.route('/')
def home():
   return render_template('index.html')

if __name__ == "__main__":
    #for e in readPktSync():
    #    print(e)
    app.run(debug=True, use_reloader=True, host="0.0.0.0")
        
                    
    