import socket
import struct
import sys
from random import randrange
import time

packer = struct.Struct('1s I')
status = ''

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:

    try:
        server_addr = (sys.argv[1], int(sys.argv[2]))
    except IndexError:
        print("Specify a server address in args! (localhost 10000)")
        sys.exit(1)
    
    def get_server_response(op, number):
        values = (op.encode(), number)
        packed_data = packer.pack(*values)
        wait_in_sec = randrange(1, 5)
        time.sleep(wait_in_sec)
        client.sendall(packed_data)
        data = client.recv(packer.size)
        unpacked_data = packer.unpack(data)
        print("Unpacked data: ", unpacked_data)
        response = unpacked_data[0].decode()
        if response == 'V' or response == 'K':
            client.close()
            exit(0)
        return response

    def binary_search():
        low = 1
        high = 100
        mid = 0

        while low <= high:
            mid = (high + low) // 2

            if get_server_response('>', mid) == 'I':
                low = mid + 1
            elif get_server_response('<', mid) == 'I':
                high = mid - 1
            else:
                get_server_response('=', mid)
                return mid

        

    client.connect(server_addr)
    
    result = binary_search()
    
    print("A keresett szam: " + str(result))

    client.close()