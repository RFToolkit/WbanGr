import re
import time

while True:
    with open('./wpan.pcap', 'rb') as file:
        byt=file.readlines()
        for i in range(len(byt)):
            yt=byt[i]
            print(yt)
        
        time.sleep(5)