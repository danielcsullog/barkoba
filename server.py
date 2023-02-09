import socket
import struct
import select
from random import randrange
import sys

packer = struct.Struct('1s I')
random_num = randrange(1,100)
is_random_number_found_by_clients = False

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:

    try:
        server_addr = (sys.argv[1], int(sys.argv[2]))
    except IndexError:
        print("Add meg a szerver cimet az argumentumokban! (localhost 4000)")
        sys.exit(1)

    server.bind(server_addr)
    server.listen(10)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sockets = [server]

    print("A gondolt szam: ", random_num)

    while True:
        readable, writable, exceptional = select.select(sockets, sockets, sockets, 1)

        if not (writable or readable or exceptional):
            continue

        for socket in readable:
            if socket is server:
                client, client_addr = socket.accept()
                sockets.append(client)
                print("Csatlakozott: ", client_addr) 
            else:
                data = socket.recv(packer.size)
                if not data:
                    sockets.remove(socket)
                    socket.close()
                    print("Kilepett")
                    if len(sockets) == 1:
                        random_num = randrange(1,100)
                        print("Az uj gondolt szam: ", random_num)
                        is_random_number_found_by_clients = False
                else:
                    unpacked_data = packer.unpack(data)
                    print("Kapott uzenet: ", unpacked_data)
                    client_tip_num = unpacked_data[1]
                    client_tip_operator = unpacked_data[0].decode()
                    response = ('', 0)

                    if is_random_number_found_by_clients == True:
                        response = ('V'.encode(), 0)
                    else:
                        if client_tip_operator == '=':
                            condition = eval(str(client_tip_num) + '==' + str(random_num))
                            if condition:
                                response = ('Y'.encode(), 0)
                                is_random_number_found_by_clients = True
                            else:
                                response = ('K'.encode(), 0)
                        else:
                            condition = eval(str(random_num) + client_tip_operator + str(client_tip_num))
                            if condition:
                                response = ('I'.encode(), client_tip_num)
                            else:
                                response = ('N'.encode(), client_tip_num)

                    packed_data = packer.pack(*response)
                    socket.sendall(packed_data)
                    