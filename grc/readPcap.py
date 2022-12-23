"""
This file is part of readPcap.
    yaml is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    yaml is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with yaml.  If not, see <https://www.gnu.org/licenses/>.
"""
from scapy.all import *
from deep_translator import GoogleTranslator, MyMemoryTranslator
from pprint import pprint
import time
from datetime import date
import io
import os
import magic
import json
import bleSniffer
from itertools import cycle
from pydub import AudioSegment
from pydub.playback import play
from scipy.io import wavfile
import numpy as np
import sys
import io
import chardet
from scapy.layers.dot15d4 import Dot15d4Data, Dot15d4Cmd
from scapy.layers.sixlowpan import *
from flask_cors import CORS,cross_origin
from flask_apscheduler import APScheduler
from flask import Flask, Response, request, render_template
from calcW import tcp, getGUDID
from Coap import COAP
from core.regle import REGLE
#from CalculWeigthBetweenTwoHexString.build.calcWeight import btfMain, xorBTF

import base64

mime = magic.Magic(mime=True)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    static_folder='web/static',
    template_folder='web'
)
CORS(app, support_credentials=True)

global rm
rm=False
rdata=b''

conf.dot15d4_protocol = "sixlowpan"
yandex = GoogleTranslator(source='auto', target='fr')


class Config:
    """App configuration."""

    JOBS = [
        {
            "id": "job1",
            "func": "readPcap:job1",
            "args": (),
            "trigger": "interval",
            "seconds": 30,
            "max_instances": 2
        }
    ]

    SCHEDULER_API_ENABLED = True

occuped=False
def job1():
    """Demo job function.
    :param var_two:
    :param var_two:
    """
    """
    global occuped
    try:
        if not occuped:
            occuped=True
            with open('.payload', 'rb') as the_file:
                oframe=the_file.read()
                if len(oframe):
                    print("[ORIGINAL FRAME]::::::::::::::::::::::::::::::::", oframe)
                    res=xorBTF(oframe.hex(), ROOT_DIR+"/perso/7-more-passwords.txt", ROOT_DIR+"/dict/med.txt")
                    print("[DECRYPT]::::::::::::::::::::::::::::::::", res)

                    with open('.secret', 'a+') as the_secret:
                        the_secret.write(res)

                #with open('{}/perso/7-more-passwords.txt'.format(ROOT_DIR), 'rb') as key:
                #    for k1 in key.readlines():
                #        k1=k1.replace(b'\n', b'')
                #        o,k=oframe, k1
                #        str_t = many_byte_xor(o, k)
                #        hexdump(str_t)
                occuped=False
    except Exception as e:
        print(e)
        pass
    """
    pass

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

color=lambda x, c=bcolors.OKGREEN: '\x1b[0m' + c + str(x) + '\x1b[0m'

def remove(rm):
    if rm:
        rm=False
        os.system('echo > '+ ROOT_DIR + "/wpan.pcap")
        return False
    return True

def ascii(din):
    return 'abcdefghijklmnopqrstwxyz'

def execXOR(line, k1):
    return ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(str(line), cycle(str(k1)))).encode('latin-1', errors='replace').replace(b"?", b" ").decode('utf-8', 'ignore')

regex0=r'[^a-zA-Z0-9áàâäãåçéèêëíìîïñóòôöõúùûüýÿæœÁÀÂÄÃÅÇÉÈÊËÍÌÎÏÑÓÒÔÖÕÚÙÛÜÝŸÆŒ\'\.\,]'
andRegex0=r'[a-zA-Z0-9áàâäãåçéèêëíìîïñóòôöõúùûüýÿæœÁÀÂÄÃÅÇÉÈÊËÍÌÎÏÑÓÒÔÖÕÚÙÛÜÝŸÆŒ\'\.\,]'

def decodeStr(t, l='fr'):
    try:
        if isinstance(t, str): t=t.encode('latin-1', 'ignore')
        detection = chardet.detect(t)
        encoding = detection["encoding"] if detection["encoding"] else 'utf-8'
        if isinstance(t, bytes):
            i=t.decode('utf-16', 'ignore')
            t=i.encode('utf-8', 'ignore').decode('utf-16', 'ignore')
            t=re.sub('([^\u0020-\u007E]{1})', ' \g<1>', t)
            t=GoogleTranslator(source='auto', target=l).translate(t)

        return ' '.join([*filter(lambda x: x, re.split(regex0, t)) ])
    except Exception as e:
        #print("Decode: ", e)
        pass
    return ""

def formatStr(string):
    string=re.sub('([^\u0020-\u007E]{1})', ' \g<1>', string)
    string=re.sub('é|è|ê', 'e', string)
    string=re.sub(r'Dunyu|DAn|Yue|Yi|chi|zhi|Tao|Seminyak|yun|yue|Jiao|Chong|Zhuo|Jin|Huan|Fang|Yu|yan|Zhong|Tong|Hong|yangs|Nian|Tang|Zi|ya|Liu|Hun|hua|tong|Yang|hiko|Zhi|Yan'.lower(), '', string.lower())
    string=string.replace('ying', 'ti')

    return string

def approxim(u):
    u=u.replace(' ', '')
    u=u.encode('utf-8').hex()
    uid=getGUDID(u, '/dict2.txt').split(',')[0].split(':')[1]
    return bytes.fromhex(uid).decode('utf-8')

def addition(line):
    if isinstance(line, str): line=line.encode('latin-1', 'ignore')
    txt=''
    tmp=line.hex()
    tmp=''.join([ tmp[i:i+2] if int(tmp[i:i+2], 16) > int('1f', 16) and tmp[i:i+2].lower() != '7f' else ',' for i in range(0,len(tmp), 2) ])
    tmp=tmp.split(',')
    res=''
    for h in tmp:
        if len(h):
            h=tcp(h)[0]
            h=' '.join([*filter(lambda x: x, re.split(r'[^a-zA-Z]', h)) ])
            txt+=approxim(h).replace('\n', ' ')+" "

    return txt

def additionV1(line):
    if isinstance(line, bytes): line=line.decode('latin-1', 'ignore')
    line=decodeStr(line)
    l=re.split(r'[a-zA-Z]',  line)
    r=[*filter(lambda x: approxim(x) if x != "" else None, list(re.split(r'[^a-zA-Z]', line))) ]
    lt=[]

    for k,v in enumerate(l):
        v=v.encode('big5-HKSCS', 'ignore')
        tmp=tcp(v.hex())
        if len(tmp[1]) and len(tmp[0]) > tmp[1][1]:
            inData=tmp[0].split(tmp[0][tmp[1][0]:tmp[1][1]-1])
            lt+=[ approxim(e).replace('\n', ' ').encode('utf-8') for e in inData ]
        elif len(v):
            v=v.decode('utf-8', 'ignore')
            lt+=[ approxim(v).replace('\n', ' ').encode('utf-8') ]

    r=[bytes(x.encode('latin-1')) if not isinstance(x, bytes) else x for x in r ]
    lt=[bytes(x.encode('latin-1'))if not isinstance(x, bytes) else x  for x in lt ]
    return (b' '.join(lt+r)).decode('latin-1', 'ignore')

def encodingUnpack(line):
    try:
        if isinstance(line, str): line=line.encode('latin-1', 'ignore')
        detection = chardet.detect(line)
        encoding = detection["encoding"] if detection["encoding"] else 'latin-1'
        ids=''
        o=line
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
                    line=tsTxt.encode('utf-16be', 'ignore').replace(rb'(\x00){2,}', b'').replace(rb'(\x20){2,}', b'') #.replace(rb'(\x00)+', b'').replace(b'\x20', b'')
                    tsTxt=line.decode('utf-8', 'ignore')
                    line=line.decode('utf-16be', 'ignore')
                    line=tsTxt+line
                    line=line.replace(r'\s{2,}', '').strip()
                line=line.replace('ying', 'ti')

            if (line):
                line=GoogleTranslator(source='auto', target='fr'
                    ).translate(line)

                # GUID
                ids=getGUDID(line.encode('utf-8', 'ignore').hex()[4:4+8])
                print(ids)
                line=' '.join([*filter(lambda x: x, re.split(regex0, line)) ])
                
                
            #hexdump(ids+line+addition(o))

            return ids+line

    except Exception as e:
        print("Main: ", e)
        pass
    return 0



def translate(line, res):
    ro="0069sandra4152"
    xorWord = lambda ss,cc: ''.join(chr(ord(s)^ord(c)) for s,c in zip(ss,cc*100))
    with open('.payload', 'a+') as the_file:
        the_file.write(xorWord(line.decode('utf-8', 'ignore'), ro))
    try:
        line=encodingUnpack(line)
        if(len(line)):
            res['payload']=line
            res['type']=stype=str(mime.from_buffer(line))
            yield res
        else:
            line=encodingUnpack(line)
            if(len(line)):
                res['payload']=line
                res['type']=stype=str(mime.from_buffer(line))
                yield response
    except:
        pass
    
    return line

def liveUDPResolver(payload, on=0, tmp=''):
    if isinstance(payload, str): payload=payload.encode('latin-1', 'ignore')
    print(payload.decode('utf-8', 'ignore'))
    state=["31392e31322e3232"]

    spVal=bytes.fromhex(state[on]).decode('utf-8', 'replace')
    print(spVal)
    payload=tcp(payload.hex(), state[on])[0]
    payload=payload.split(spVal)
    if on > -1:
        print(''.join(payload).encode('utf-8', 'ignore').decode('utf-8', 'ignore'))
        for i in range(len(payload) -1):
            print(i)
            tmp+=payload[i]
            return liveUDPResolver(tmp, on)

    if on < 1:
        print(payload)
        return (re.split(regex0, payload) + re.split(andRegex0, payload))

    on-=1
    
    
def readPktSync():
    try:
        pkts=rdpcap(ROOT_DIR + "/wpan.pcap")
        for pk in pkts:
            for sub in pk:
                rm=False
                for p in sub:
                    if p:
                        src,dst,panid=None, None, None
                        if Dot15d4FCS in p:
                            if Dot15d4Data in p:
                                src=p[Dot15d4Data].src_panid
                                dst=p[Dot15d4Data].dest_panid
                                if src != None: src=hex(int(src))
                                if dst != None: dst=hex(int(dst))
                                
                            if Dot15d4Beacon in p:
                                #print(p[Dot15d4Beacon])
                                panid = hex(int(p[Dot15d4Beacon].src_panid))
                                print("PanID", panid)
                            """
                            if SixLoWPAN in p:
                            if LoWPANFragmentationFirst in p:
                            if LoWPANFragmentationSubsequent in p:
                            if LoWPANMesh in p:
                            if LoWPAN_IPHC in p:
                                print(SixLoWPAN(p))
                            """


                            
                            

                        payload=b''
                        if (p.payload.payload and len(p.payload.payload)):

                            reversedBytes = bytes(p.payload.payload)

                            """dt=date.today().isoformat().encode('utf-8', 'ignore').hex()
                            payload=tcp(payload.hex(), dt)[0]
                            payload=payload.encode('utf-8', 'ignore')"""

                            if len(reversedBytes) >8:
                                coap=COAP(reversedBytes)
                                cph=coap.noCipherredData()
                                if cph:
                                    t=coap.getCode()
                                    s=int((cph[2:4] + cph[5:7]), 2)
                                    if cph[8:s*2] != '':
                                        
                                        path=str(int(cph[8:s*2], 2))
                                        if path == '': path='00'
                                        path=str(int(path, 16))
                                        path=coap.hexToByteString(path)
                                        ###### PAYLOAD ######
                                        payload=str(int(cph[s*2:], 2))
                                        payload=str(int(payload, 16))
                                        payload=coap.hexToByteString(payload)
                                        unit=[int(payload.hex()[i:i+2], 16) for i in range(0, len(payload.hex()), 2)]
                                        #payload=[ *translate(b''.join(payload), {  "src": src, "dst": dst, "panid": panid }) ]
                                        
                                        if t == 1: 
                                            print('========= GET ===========')
                                        if t == 2:
                                            print('========= POST ==========')
                                        if t == 3:
                                            print('========= PUT ============')
                                        if t == 4:
                                            print('========== DELETE ==========')
                                        
                                        print("x"*35)
                                        if src or dst: print(src, " -> ", dst)
                                        if panid: print("PanID", panid)
                                        print("x"*35)
                                        print("TYPE", str(mime.from_buffer(reversedBytes)))
                                        print("x"*35)
                                        print("CODE: ", t)
                                        print("MID: ", coap.getMessageID())
                                        print("Size: ", s)
                                        print("Path: /"+ "/".join(decodeStr(path).split(' ')))
                                        print("Data: ", payload.hex())
                                        #print( str(mime.from_buffer(reversedBytes)) )
                                        activate=0
                                        unitNum=[*map(lambda x: x < 58 and x > 47, unit)]
                                        #for k, v in enumerate(unit):
                                        #    if v == 86:
                                        #        print(''.join([ chr(x) for x in unit[k-3:k+1] ]).replace('\n', '').replace('\t', '').replace('\r', ''))

                                        """if hexf == 86 and len(unitNum[i:k]) and bool(sum(unitNum)):
                                                print(unitNum[i:k].reverse())
                                                val=unitNum[i:k].index(True)
                                                print(unit[i+val:k])
                                                print('UNIT: ', ''.join([ chr(x) for x in unit[i+val:k] ]))
                                                i=k"""
                                        
                                        #import base64
                                        a=b''.join([ n.to_bytes(3, byteorder='little') for n in unit ])
                                        print("Message1: ", decodeStr(payload))
                                        print("ORIGINAL D:", payload.decode('utf-8', 'ignore'))
                                        
                                        #print(liveUDPResolver(payload, 0))
                                        #payload=' '.join([*filter(lambda x: x, liveUDPResolver(payload, 2))]).encode()
                                        #print("Message2: ", decodeStr(payload))
                                        from bs4 import UnicodeDammit
                                        suggestion = UnicodeDammit(payload)
                                        #https://datatracker.ietf.org/doc/rfc7752/
                                        bgpName=payload.hex().find('1026')
                                        if (bgpName >= 0):
                                            print('    ','*'*30)
                                            try:
                                                encoding=suggestion.original_encoding or 'utf-8'
                                                payload=payload.decode(encoding, 'ignore')
                                                print("Message2: ", encodingUnpack(payload))
                                                nameLength=payload.encode().hex()[bgpName:bgpName+8]
                                                nameLength=int(nameLength, 16)
                                                name=payload[bgpName+8:bgpName+16]
                                                if len(name):
                                                    print("++++DEVICE NAME: ", name)
                                            except:
                                                pass
                                        res=decodeStr(payload).split(' ')
                                        if 'WAN' in res:
                                            wanName=res[res.index('WAN') + 1]
                                            print("++++WAN NAME: ", wanName)

                                        if isinstance(payload, str): payload=payload.encode() 
                                        #tt=xorBTF(payload.hex(), ROOT_DIR+"/perso/1000000-password-seclists.txt", ROOT_DIR+"/o.txt")
                                        #tt=set([ x for x in [*filter(lambda x: x, tt.split(";")) ] ])
                                        #print(tt)

                                        for i in REGLE.keys():
                                            if payload.hex().__contains__(i):
                                                if (activate == 0):
                                                    print("Electrode state: ")
                                                    activate=-1
                                                print(REGLE[i])
                                            
                                        """
                                        print("Message: ",  decodeStr(payload.decode('latin-1', 'ignore')))
                                        payload=payload.decode('utf-8', 'ignore')
                                        pay=b''.join([ bytes( chr(ord(payload[e])%25).encode() ) for e in range(len(payload)) ])
                                        print("Message2: ", decodeStr( pay))
                                        """
                                        #t=[ t[i:i+2] for i in range(0, len(t), 2) ]
                                        #t=[ bin(int(x, 16))[2:] for x in t ]
                                        
                        res=translate(payload, {  "src": src, "dst": dst, "panid": panid })
                        #print([ str(mime.from_buffer(x['payload'])) for x in [*res] ])
                        for edt in res:
                            yield json.dumps(edt)
    
    except Exception as e:
        #print(e)
        pass
    #finally:
    #    print("==========================================End")

@app.route("/getpkt")
def hello_world():
    print('in')
    return Response(readPktSync(), mimetype="application/json")

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/getble')
async def getble():
    rp=await bleSniffer.Scan()
    for i in range(len(rp)):
        rp[i]['manufact']=additionV1(rp[i]['manufact'])+addition(rp[i]['manufact'])
        rp[i]['services']=additionV1(rp[i]['services'])+addition(rp[i]['services'])

        if len(rp[i]['manufact']): hexdump(rp[i]['manufact'])
        if len(rp[i]['services']): hexdump(rp[i]['services'])

    print(json.dumps(rp))
    return json.dumps(rp)

if __name__ == "__main__":
    print('Please run gnuradio')
    while True:
        try:
            for e in readPktSync():
                print(e)
        except KeyboardInterrupt:
            break

        time.sleep(5)
    """
    app.config.from_object(Config())

    scheduler = APScheduler()
    # it is also possible to enable the API directly
    
    scheduler.api_enabled = True  # noqa: E800
    scheduler.init_app(app)
    scheduler.start()
    """
    #app.run(debug=True, use_reloader=True, host="0.0.0.0", port="5000")
        
                    
    
