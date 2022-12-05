import os
from CalculWeigthBetweenTwoHexString.build .calcWeight import getMatchingCase

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
with open("/tmp/new.pcap", "rb") as f:
    p=f.read()
    while p:
        for i in range(len(p)//32):
            print( getMatchingCase(str(p.hex()[i*32:32+32*i]), ROOT_DIR+ "/id") )