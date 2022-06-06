import json
import serial
from .utils import crc15

OK = 0
ERR_DEFAULT = -1
ERR_READ = -2
ERR_CRC = -3

status = {
    0: "closed",
    1: "open",
    2: "short",
    3: "sabotaged"
}

status_bits = {
    0b00: 0,
    0b10: 1,
    0b01: 2,
    0b11: 3
}

class RL_Board:

    def __init__(
        self,
        port="/dev/ttyUSB0", 
        baudrate=115200,
        address = 1,
        timeout = 2
    ):
        # Defaults
        self.cmd_filename = "lib/commands.json"
        self.counter = 1
        # Load command infos from file
        self._load()
        # Set serial parameters
        self.port = port
        self.baudrate = baudrate
        self.address = address
        self.timeout = timeout


    def _load(self):
        cmd_content = open(self.cmd_filename).read()
        self.commands = json.loads(cmd_content)


    def open(self):
        self.serial = serial.Serial(
            port = self.port, 
            baudrate = self.baudrate,
            timeout = self.timeout
        )
        self.serial.flushInput()
        self.serial.flushOutput()


    # def log(self):
    #     print(self.counter)


    def add_counter(self):
        if(self.counter != 255):
            self.counter+=1
        else:
            self.counter=1


    def _check_crc(self, packet):
        crc_packet = packet[1:-2]
        crc_received = packet[-2:]
        crc_calc = crc15(crc_packet, len(crc_packet))
        
        return (crc_received == crc_calc.to_bytes(2, 'little'))


    def read_inputs(self):
        name = "read_inputs"
        if(self.serial.isOpen()):
            packet = bytearray()
            cmd = bytearray.fromhex(self.commands[name]["hex_cmd"])

            packet.append(self.address)
            packet.extend(cmd)
            packet.append(self.counter)

            crc_packet = packet[2:]
            crc = crc15(crc_packet, len(crc_packet))
            crc = bytearray(crc.to_bytes(2, 'little'))
            packet.extend(crc)
            
            self.serial.write(packet)
            res = self.serial.read(18) # Read 18 bytes from buff
            
            if(self._check_crc(res)):
                self.add_counter()
                inputs = []
                inputs_bytes = res[4:16]
                # print(inputs_bytes.hex(), len(inputs_bytes))
                for in_byte in inputs_bytes:
                    # print(bin(in_byte), end=' ')
                    in_status = (in_byte & 0b11000000)>>6
                    in_status = status_bits[in_status]
                    in_counter = (in_byte & 0b00111111)
                    in_counter = int(in_counter)
                    in_struct = {
                        "status": in_status,
                        "counter": in_counter
                    }
                    inputs.append(in_struct)
                return (inputs, 0)
            else:
                return (None, ERR_CRC)

        else:
            return (None, ERR_READ)