class COAP():

    def __init__(self, bytesA):
        self.bytesArrays=bytesA
        self.bytesToString=[ bin(x)[2:] for x in bytesA ]

    ########### Methods #############

    def hexToByteString(self, chain):
        return b''.join([ chr(int(chain[i:i+2], 16)).encode('latin-1', 'ignore') for i in range(0, len(chain), 2) ])

    def byteToString(self):
        return ''.join(self.bytesToString)

    ####################################End
    
    def version(self):
        return int(self.byteToString()[0:1], 2)

    def T(self):
        return int(self.byteToString()[2:3], 2)

    def TKL(self):
        return int(self.byteToString()[4:7], 2)

    def getCode(self):
        classe=int(self.byteToString()[8:11], 2)
        details=int(self.byteToString()[11:15], 2)
        return (100*classe) + details

    def getMessageID(self):
        return hex(int(self.byteToString()[16:31], 2))[2:]

    def noCipherredData(self):
        res=None
        if self.TKL() == 0 and len(self.byteToString()) > 31:
            res=self.byteToString()[31:]
            res=[ *filter(lambda x: x, [ bin(int(res, 2))[2:][i:i+2] for i in range(0, len(res), 2) ]) ]
            res=''.join(res)

        return res

    def initAPP(cph):
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

    

    