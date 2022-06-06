# Calculate CRC
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
