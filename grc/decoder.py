def nrzs(nrz):
    NRZS = []
    state = nrz[0]
    for bit in nrz:
        state ^= bit ^ 1
        NRZS.append(state)
    return NRZS

def nrzi(data):
    nrzi=""
    for i in range(len(data)):
        if i==0:
            if data[i] == '0': nrzi+= "0"
            else: nrzi+="01"
            
        elif( data[i] == '0'):
            if nrzi[i*2-1] == '0': nrzi += "00"
            else: nrzi += "11"

        elif data[i] == '1':
            if nrzi[i*2-1] == '0': nrzi += "01"
            else: nrzi += "10"

    return nrzi

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

    r=''.join([ chr(x) for x in bytes])  # Output: [170]
    return r

test='1111010'
print(nrzi(test))
print('1110010')