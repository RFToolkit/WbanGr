from CalculWeigthBetweenTwoHexString.build.calcWeight import getEntry, getEntryMatch, getMatchingCase
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def getGUDID(hex):
    return getMatchingCase(hex, ROOT_DIR+"/uid.csv")

def tcp(ws, s="", pos=None):
    try:
        res=0
        err=-1
        r=None
        if(len(s)==0):
            r=getEntry(ws).split(',')
        else:
            r=getEntryMatch(ws, s).split(',')
        if pos: r[-1]=pos
            
        xored=r[2].split(';')

        mpkg=ws[0:int(r[-1])][::1]
        nch=''

        for i in range(0, len(mpkg), 2):
            p=int(xored[i%len(xored)]) ^ int(mpkg[i:i+2], 16)
            if (p >= int(xored[i%len(xored)+1])):
                nch=chr(p - int(xored[i%len(xored)+1]))+nch
            else:
                nch=chr(p + int(xored[i%len(xored)+1]))+nch


        mpkg=ws[int(r[-1]):int(r[-1])+len(r[1])]

        for i in range(0, len(xored), 2):
            p=int(xored[i]) ^ int(mpkg[i:i+2], 16)
            if (p >= int(xored[i+1])):
                nch+=chr(p - int(xored[i+1]))
            else:
                nch+=chr(p + int(xored[i+1]))

        mpkg=ws[int(r[-1])+len(r[1]):]

        for i in range(0, len(mpkg), 2):
            p=int(xored[i%len(xored)]) ^ int(mpkg[i:i+2], 16)
            if (p >= int(xored[i%len(xored)+1])):
                nch+=chr(p - int(xored[i%len(xored)+1]))
            else:
                nch+=chr(p + int(xored[i%len(xored)+1]))

        return [ nch, [int(r[-1]), int(r[-1])+len(r[1])] ]
    except:
        pass
    
    return ["", []]
