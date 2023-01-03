# BYTES
try:
    from precompiled.calcWeight import btfMain, xorBTF
except:
    from calcWeight import btfMain, xorBTF
from calcW import getGUDID, tcp
import os
import re
from calcW import tcp

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def approxim(u):
    u=u.replace(' ', '')
    u=u.encode('utf-8').hex()
    uid=getGUDID(u, '/perso/dict2.hex')
    uid=uid.split(',')[0].split(':')[1]
    uid=bytes.fromhex(uid).decode('utf-8')
    print(uid)

    return uid

def addition(line):
    if isinstance(line, str): line=line.encode('latin-1', 'ignore')
    txt,bis='', ''
    tmp=line.hex()
    tmp=''.join([ tmp[i:i+2] if int(tmp[i:i+2], 16) > int('1f', 16) and tmp[i:i+2].lower() != '7f' else ',' for i in range(0,len(tmp), 2) ])
    tmp=tmp.split(',')
    res=''
    for h in tmp:
        if len(h):
            test=approxim(h).replace('\n', ' ')+" "
            if test != bis:
                #h=tcp(h)[0]
                #h=' '.join([*filter(lambda x: x, re.split(r'[^a-zA-Z]', h)) ])
                bis=test
                txt+=bis

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



def nrzi(chaineCourrante):
    c=chaineCourrante
    tmp=''
    j=0
    while j < len(chaineCourrante):
        if j != 0:
            c=chaineCourrante[j:]
            if chaineCourrante[j-1] == '0' and chaineCourrante[j] == '1':
                i=c[1:].find('1')
                tmp+='0'*i
            elif c.startswith('0'):
                i=c.find('1')
                tmp+='0'*(i+1)
            else:
                i=c.find('0')
                tmp+='1'*(i+1)
        else: tmp=chaineCourrante[j]
        j+=len(tmp)
    
    print(tmp)

import codext
e='20920412181459055359906169385951366427436639'
e=tcp(e)[0]
print(e)

print(codext.guess(e, "affine"))

"""
e='20920412181459055359906169385951366427436639153325995766791629908616221559689774898356804069271773348479563339756002598627139601443834731879854242908865200192348194607950338839100653738492302633578364685746375622140128656343676678639979769083475125899370570029574048882336403458126950'
e=tcp(e, "udp://".encode().hex())[0]
print(e)

print(codext.guess(e))

e='20920412181459055359906169385951366427436639153325995766791629908616221559689774898356804069271773348479563339756002598627139601443834731879854242908865200192348194607950338839100653738492302633578364685746375622140128656343676678639979769083475125899370570029574048882336403458126950'
e=tcp(e, "coap://".encode().hex())[0]
print(e)

e='20920412181459055359906169385951366427436639153325995766791629908616221559689774898356804069271773348479563339756002598627139601443834731879854242908865200192348194607950338839100653738492302633578364685746375622140128656343676678639979769083475125899370570029574048882336403458126950'

e=tcp(e, "http://".encode().hex())[0]
print(e)

e='20920412181459055359906169385951366427436639153325995766791629908616221559689774898356804069271773348479563339756002598627139601443834731879854242908865200192348194607950338839100653738492302633578364685746375622140128656343676678639979769083475125899370570029574048882336403458126950'
e=tcp(e, "https://".encode().hex())[0]
print(e)

e='20920412181459055359906169385951366427436639153325995766791629908616221559689774898356804069271773348479563339756002598627139601443834731879854242908865200192348194607950338839100653738492302633578364685746375622140128656343676678639979769083475125899370570029574048882336403458126950'
e=tcp(e, ".com".encode().hex())[0]
print(e)
"""

#print(codext.guess(e))

"""import nltk

encoded_bytes = 

def m(encoded_bytes):
    # Split the encoded bytes into individual bits
    bits = []
    for b in encoded_bytes:
        for i in range(8):
            bits.append((b >> i) & 1)

    # Determine the value of each bit
    decoded_bits = []
    for bit in bits:
        if bit == 1:
            decoded_bits.append(1)
        else:
            decoded_bits.append(0)

    # Convert the bits to bytes
    bytes = []
    for i in range(0, len(decoded_bits), 8):
        byte = decoded_bits[i:i+8]
        bytes.append(int("".join(str(b) for b in byte), 2))

    print([ chr(x) for x in bytes])  # Output: [170]"""

"""with open('output2.bin', 'rb') as l:
    for d in l.readlines():
        
        #res=xorBTF(d.hex(), ROOT_DIR+"/perso/1000000-password-seclists.txt", ROOT_DIR+"/perso/dict.txt")
        #print(res)
        tokens = nltk.sent_tokenize(d.decode('utf-8', 'ignore').lower())
        print(tokens)"""

"""from scapy.all import *
import pyshark
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ro="007leouf"
p=len(ro)
xorWord = lambda ss,cc: ''.join(chr(ord(s)^ord(c)) for s,c in zip(ss,cc*100))

l={ "m0", "" }

def readPktSync():
    for e in l:
        i=e.split(' ')[-1].replace('\n', '')
        try:
            o='\x85SF\x11W\x12Hg\x10Y8v#\x91\x16\tHQ84$\x90\x06y\x01\x02'
            encrypt = xorWord(o, i).replace('\t', '')
            print(encrypt)
        except Exception as e:
            print(e)
            pass

readPktSync()"""
#from calcW import getGUDID



"""
u='bt b y i b wt K FB O M H B msb d'
u=u.replace(' ', '')
u=u.encode('utf-8').hex()
"""
#print(getGUDID(u, './perso/'))

"""
with open('./dict/med.txt', 'rb') as d:
    with open('./dict/base.hex', 'w') as d2:
        for e in d.readlines():
            d2.write(e.hex()+"\n")

print(u)


import os
from CalculWeigthBetweenTwoHexString.build .calcWeight import getMatchingCase

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
with open("/tmp/new.pcap", "rb") as f:
    p=f.read()
    while p:
        for i in range(len(p)//32):
            print( getMatchingCase(str(p.hex()[i*32:32+32*i]), ROOT_DIR+ "/id") )
"""