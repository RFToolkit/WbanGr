#/usr/bin/env python

#from deep_translator import DeeplTranslator
from deep_translator import GoogleTranslator
#from scapy.all import *
from itertools import cycle
import magic
import fileinput
import binascii
import datetime
import socket
import time
import re
import base64
import os
#from pydub import AudioSegment
#from pydub.playback import play
#from scipy.io import wavfile
#import numpy as np
#import sys
#import io

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
#yandex= DeeplTranslator(source='zh', target='fr', api_key="16ee3099-d38a-4b50-594b-fce1d74b0132", use_free_api=False)

yandex = GoogleTranslator(source='zh-TW', target='fr')

def bit_flipping(payload):
    for i in range(len(payload)):
        # 1 bit flip - 8 permutations per byte
        for j in range(8):
            copy = bytearray(payload)
            copy[i] = copy[i] ^ (1<<j)
            yield bytes(copy)  # ''.join(chr(c) for c in copy)

        # 2 bits flip - 7 permutations per byte
        for j in range(7):
            copy = bytearray(payload)
            copy[i] = copy[i] ^ (0b11000000 >> j)
            yield bytes(copy)  # ''.join(chr(c) for c in copy)
    
        # 4 bits flip - 5 permutations per byte
        for j in range(5):
            copy = bytearray(payload)
            copy[i] = copy[i] ^ (0b11110000 >> j)
            yield bytes(copy)  # ''.join(chr(c) for c in copy)

def byte_flipping(payload):
    # 1 byte flip
    for i in range(len(payload)):
        payload_copy = bytearray(payload)
        payload_copy[i] = payload_copy[i] ^ 0xFF
        yield payload_copy

    # 2 byte flip
    for i in range(len(payload)-1):
        payload_copy = bytearray(payload)
        payload_copy[i] = payload_copy[i] ^ 0xFF
        payload_copy[i+1] = payload_copy[i+1] ^ 0xFF
        yield payload_copy

    # 4 byte flip
    for i in range(len(payload)-3):
        payload_copy = bytearray(payload)
        payload_copy[i] = payload_copy[i] ^ 0xFF
        payload_copy[i+1] = payload_copy[i+1] ^ 0xFF
        payload_copy[i+2] = payload_copy[i+2] ^ 0xFF
        payload_copy[i+3] = payload_copy[i+3] ^ 0xFF
        yield payload_copy

def known_integers(payload):

    known_2_byte_int = (
        bytearray(b'\x01\x00'),  # 256 be
        bytearray(b'\x00\x01'),  # 256 le
        bytearray(b'\x04\x00'),  # 1024 be
        bytearray(b'\x00\x04'),  # 1024 le
        bytearray(b'\x10\x00'),  # 4096 be
        bytearray(b'\x00\x10'),  # 4096 le
        bytearray(b'\x54\x0a'),  # T
        bytearray(b'\x43\x0a'),  # C
        bytearray(b'\x47\x0a'),  # G
    )

    for i in range(len(payload)-1):
        for known_int in known_2_byte_int:
            payload_copy = bytearray(payload)
            yield payload_copy[:i] + known_int + payload_copy[i+2:]


    known_8_byte_int = (
        bytearray(b'\x7f\xff\xff\xff\xff\xff\xff\xff'),  # python max_int be
        bytearray(b'\x7f\xff\xff\xff\xff\xff\xff\xfe'),  # python max int -1 be
        bytearray(b'\xff\xff\xff\xff\xff\xff\xff\x7f'),  # python max_int le
        bytearray(b'\xfe\xff\xff\xff\xff\xff\xff\x7f'),  # python max_int -1 le
        bytearray(b'\x65\x65\x67\x0a\xff\xff\xff\x7f'),  # EEG
        bytearray(b'\x65\x6d\x67\x0a\xff\xff\xff\x7f'),  # EMG
        bytearray(b'\x65\x6b\x67\x0a\xff\xff\xff\x7f'),  # EKG
        bytearray(b'\x65\x63\x67\x0a\xff\xff\xff\x7f'),  # ECG
        bytearray(b'\x70\x69\x6e\x67\xff\xff\xff\x7f'),  # ping
        bytearray(b'\x70\x6f\x6e\x67\xff\xff\xff\x7f'),  # pong
        bytearray(b'\x6a\x6f\x69\x6e\xff\xff\xff\x7f'),  # join
        bytearray(b'\x70\x75\x62\xff\xff\xff\xff\xff'),  # pub
        bytearray(b'\x73\x75\x62\xff\xff\xff\xff\xff'),  # sub
        bytearray(b'\x73\x70\x4f\x32\xff\xff\xff\xff'),  # spO2
        bytearray(b'\x65\x6d\x6d\x61\x72\x69\x6f\xff'),  # spO2
    )
    
    for i in range(len(payload)-7):
        for known_int in known_8_byte_int:
            payload_copy = bytearray(payload)
            yield payload_copy[:i] + known_int + payload_copy[i+8:]

def insert_in_between_bytes(payload, character=0x41):
    for i in range(len(payload)):
        payload = bytearray(payload)
        for inject_len in (4, 8, 16, 32, 64, 128):
            yield payload[:i] + bytearray([character]*inject_len) + payload[i:]

def msg_len_adjustment(msg):
    return (len(msg)).to_bytes(4, byteorder='big') + msg[:21] + str(len(msg)).zfill(4).encode() + msg[25:]

def all_cases(payload):
    for case in bit_flipping(payload):
        yield case
    for case in byte_flipping(payload):
        yield case
    for case in known_integers(payload):
        yield case
    for case in insert_in_between_bytes(payload):
        yield case

def many_byte_xor(buf, key):
    buf = bytearray(buf)
    key = bytearray(key)
    key_len = len(key)
    for i, bufbyte in enumerate(buf):
        buf[i] = bufbyte ^ key[i % key_len]
    return buf

def execXOR(line, k1):
    return ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(str(line), cycle(str(k1)))).encode('latin-1', errors='replace').replace(b"?", b" ").decode('utf-8', 'ignore')

######################################################

def translate(line):
    res=line.decode('big5', 'ignore')
    res=re.sub('([^\u0020-\u007E]+)', ' \g<1> ', res)
    res=re.sub('\s+', ' ', res)
    print('x'*35)
    time.sleep(0.6)
    res=str(yandex.translate(res))
    res=re.sub('é|è|ê', 'e', res)
    res=re.sub('â|à', 'a', res)
    res=res.encode('gbk', 'ignore')
    res=res.decode('ascii', 'ignore')

    yield res

def process_packets(infile):
    pkts = rdpcap(infile)
    cooked=[]
    for p in pkts:
        pkt_payload = str(p.payload.payload)
        pkt_offset = pkt_payload[:3]
        if pkt_payload and pkt_offset:
            p.payload.payload=many_byte_xor(pkt_payload, pkt_offset)
            yield p.payload

##########################################

if __name__ == '__main__':
    mime = magic.Magic(mime=True)
    
    for line in fileinput.input(mode="rb", openhook=fileinput.hook_encoded("utf-16be", "ignore")):
        if line:
            pkt_payload = line
            stype=mime.from_buffer(pkt_payload)
            print(stype)
            if True:
                #stype != "application/octet-stream" or stype == "text/plain":
                """print(pkt_payload)
                

                header=b'RIFF\x28\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x02\x00\x00}\x00\x00\x00\xf4\x01\x00\x04\x00\x10\x00data\x04\x00\x00\x00\x00\x00\x00\x00'
                rate, data = wavfile.read(io.BytesIO(header+pkt_payload))
                shifted = data * (2 ** 31 - 1) # Data ranges from -1.0 to 1.0
                rawdata = shifted.astype(np.int32).tobytes('F')

                sound = AudioSegment(data=rawdata, sample_width=4, frame_rate=4, channels=1)
                try:
                    play(sound)
                except:
                    pass"""
                for ts in translate(pkt_payload):
                    print(ts)
                    #print('*'*35)
            else: print(base64.b64encode(line))
            """xor=many_byte_xor(pkt_payload, pkt_payload[3:])
                print("."*35)
                print(mime.from_buffer(bytes(xor)))
                for ts in translate(xor):
                    print(ts)
            """
            #with open('{}/7-more-passwords.txt'.format(ROOT_DIR), 'r', encoding="latin-1", errors="ignore") as key:
            #    for k1 in key.readlines():
            #        str_t = execXOR(line, k1)
            #        for el in words:
            #            if el.lower() in str_t.lower():
            #                print(str_t)
            #
            #for case in all_cases(line):
            #    case = case.decode('utf-8', 'ignore')
            #    with open('{}/7-more-passwords.txt'.format(ROOT_DIR), 'r', encoding="latin-1", errors="ignore") as key:
            #        for k1 in key.readlines():
            #            str_t = execXOR(case, k1)
            #            for el in words:
            #                if el.lower() in str_t.lower():
            #                    print(str_t)
            #
            #break

            """res=GoogleTranslator(source='auto', target='fr').translate(line.decode('utf-16be', 'ignore'))
            res=res.encode("utf-8", "ignore")
            print(res.decode('utf-8', 'ignore'))"""

            """if True: #stype != "application/octet-stream":
                #print(stype)
                xored=many_byte_xor(pkt_payload, pkt_offset)
                print(xored.decode('utf-8', 'ignore').replace('\n|\s|\r|\t', ' '))
                print('\n')
                print(mime.from_buffer(bytes(xored)))

                for case in all_cases(line):
                    print(case.decode('utf-8', 'ignore').replace('\n|\s|\r|\t', ' '))
                #stype=mime.from_buffer(xored)
                #print(stype)
            """
            