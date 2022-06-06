def crc15(data, len):
    remainder = 16
    polynom = 0x4599

    for pbyte in range(0, len):
        remainder ^= (data[pbyte] << 7)
        for bit in range(8, 0, -1):
            if((remainder & 0x4000) > 0):
                remainder = (remainder << 1) & 0xFFFF
                remainder = remainder ^ polynom
            else:
                remainder = (remainder << 1) & 0xFFFF
    
    return (remainder*2) & 0xFFFF

# packet1 = b'\x01\x52\x04\x00\x10\x01\x82\x17'
# data = [0x52,0x04,0x00,0x10,0x01]
# data = b'\x04\x00\x10\x01'
data = [0x0F,0x00,0x11,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
len = 15

print("res:")
print(hex(crc15(data, len)))
