import socket
import struct
import sys
from random import randrange
import time

packer = struct.Struct('1s I')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:

    try:
        server_addr = (sys.argv[1], int(sys.argv[2]))
    except IndexError:
        print("Add meg a szerver cimet az argumentumokban! (localhost 4000)")
        sys.exit(1)

    def get_server_response(operator, number):
        values = (operator.encode(), number)
        packed_data = packer.pack(*values)
        seconds_to_wait = randrange(1, 5)
        time.sleep(seconds_to_wait)
        client.sendall(packed_data)

        server_response_data = client.recv(packer.size)
        unpacked_data = packer.unpack(server_response_data)
        print("Adat a szervertol: ", unpacked_data)
        response = unpacked_data[0].decode()

        if response == 'V' or response == 'K':
            client.close()
            exit(0)

        return response   

    client.connect(server_addr)
    
    get_server_response('=', 90)

    client.close()