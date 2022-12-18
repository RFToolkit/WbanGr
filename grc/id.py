from calcW import getGUDID

u='bt b y i b wt K FB O M H B msb d'
u=u.replace(' ', '')
u=u.encode('utf-8').hex()

#print(getGUDID(u, './perso/'))

with open('./dict/med.txt', 'rb') as d:
    with open('./dict/base.hex', 'w') as d2:
        for e in d.readlines():
            d2.write(e.hex()+"\n")

print(u)

"""
import os
from CalculWeigthBetweenTwoHexString.build .calcWeight import getMatchingCase

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
with open("/tmp/new.pcap", "rb") as f:
    p=f.read()
    while p:
        for i in range(len(p)//32):
            print( getMatchingCase(str(p.hex()[i*32:32+32*i]), ROOT_DIR+ "/id") )
"""