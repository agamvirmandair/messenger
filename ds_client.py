# AGAMVIR SINGH MANDAIR
# mandaira@uci.edu
# 40141643
import socket
import time
from ds_protocol import extract_json


def send(server: str, port: int, username: str,
         password: str, message: str, bio: str = None):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((server, port))
        send = client.makefile("w")
        recv = client.makefile("r")
        try:
            join_msg = f'''{{"join": {{"username": "{username}",
            "password": "{password}", "token": ""}}}}'''
            send.write(join_msg + '\r\n')
            send.flush()
            resp = reciever(recv)
            start = resp.index("token") + 9
            end = resp.index('"}}')
            token = resp[start:end]
            if message != '':
                post = f'''{{"token": "{token}", "post": {{"entry":
                "{message}", "timestamp": "{time.time()}"}}}}'''
                send.write(post + '\r\n')
                send.flush()
                reciever(recv)

            if bio is not None:
                post = f'''{{"token": "{token}", "bio": {{"entry":
                "{bio}", "timestamp": "{time.time()}"}}}}'''
                send.write(post + '\r\n')
                send.flush()
                reciever(recv)
            return True

        except Exception as e:
            print('Invalid JSON message')
            return False


def reciever(recv):
    response = recv.readline()
    resp = extract_json(response)
    if resp[0] == 'error':
        print(resp[1])
        raise AssertionError
    else:
        print('Message from server', resp[1])
    return response
