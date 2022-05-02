import socket
import struct


def create_connection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 6969))
    return s


def close_connection(socket):
    socket.close()


def send_option_to_server(socket, option_id):
    res = socket.send(struct.pack("!i", option_id))


def get_response_from_server(socket):
    cnt = socket.recv(4)
    # print(cnt)
    cnt = struct.unpack('!i', cnt)[0]
    return cnt
