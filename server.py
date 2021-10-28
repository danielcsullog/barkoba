import socket
import struct
import select
from random import randrange
import sys

packer = struct.Struct('1s I')

random_num = randrange(1,100)
print("A gondolt szam: ", random_num)

num_found = False

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:

    try:
        server_addr = (sys.argv[1], int(sys.argv[2]))
    except IndexError:
        print("Specify a server address in args! (localhost 10000)")
        sys.exit(1)

    server.bind(server_addr)
    server.listen(10)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sockets = [server]

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
                        num_found = False
                else:
                    unpacked_data = packer.unpack(data)
                    print("Kapott uzenet: ", unpacked_data)
                    client_tip = unpacked_data[1]
                    client_op = unpacked_data[0].decode()
                    values = ('',0)

                    if num_found == True:
                        values = ('V'.encode(), 0)
                    else:
                        if client_op == '=':
                            cond = eval(str(client_tip) + '==' + str(random_num))
                            if cond:
                                values = ('Y'.encode(), 0)
                                num_found = True
                            else:
                                values = ('K'.encode(), 0)
                        else:
                            cond = eval(str(random_num) + client_op + str(client_tip))
                            if cond:
                                values = ('I'.encode(), client_tip)
                            else:
                                values = ('N'.encode(), client_tip)

                    packed_data = packer.pack(*values)
                    socket.sendall(packed_data)
                    