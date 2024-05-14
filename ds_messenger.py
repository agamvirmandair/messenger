""" Responsible for direct message feature"""
# AGAMVIR SINGH MANDAIR
# mandaira@uci.edu
# 40141643
import socket
import time
from ds_client import reciever
from ds_protocol import direct_msg


class DirectMessage:
    """responsible for making an object for a message"""
    def __init__(self):
        self.recipient = None
        self.message = None
        self.timestamp = None


class DirectMessenger:
    ''' responsible for all the features in direct message'''
    def __init__(self, dsuserver=None, username=None, password=None):
        '''Initiaze the messenger'''
        self.token = None
        self.port = 3021
        self.server = dsuserver
        self.username = username
        self.password = password

    def send(self, message: str, recipient: str) -> bool:
        ''' send message to a user'''
        # must return true if message successfully sent, false if send failed.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((self.server, self.port))
            send = client.makefile("w")
            recv = client.makefile("r")
            try:
                join_msg = f'''{{"join": {{"username": "{self.username}",
                "password": "{self.password}", "token": ""}}}}'''
                send.write(join_msg + '\r\n')
                send.flush()
                resp = reciever(recv)
                start = resp.index("token") + 9
                end = resp.index('"}}')
                token = resp[start:end]
                directmsg = f'''{{"token":"{token}",
                "directmessage": {{"entry": "{message}","recipient\
":"{recipient}", "timestamp": "{time.time()}"}}}}'''
                send.write(directmsg + '\r\n')
                send.flush()
                reciever(recv)
                return True
            except Exception as e:
                print('Invalid JSON message', e)
                return False

    def retrieve_new(self) -> list:
        ''' retrieve a list of new messages'''
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((self.server, self.port))
            send = client.makefile("w")
            recv = client.makefile("r")
            try:
                join_msg = f'''{{"join": {{"username": "{self.username}",
                "password": "{self.password}", "token": ""}}}}'''
                send.write(join_msg + '\r\n')
                send.flush()
                resp = reciever(recv)
                start = resp.index("token") + 9
                end = resp.index('"}}')
                token = resp[start:end]
                final = f'{{"token":"{token}", "directmessage": "new"}}'
                send.write(final + '\r\n')
                send.flush()
                response = recv.readline()
                resp = direct_msg(response)
                new_messages = []
                for x in resp[1]:
                    msg = DirectMessage()
                    msg.recipient = x["from"]
                    msg.message = x["message"]
                    msg.timestamp = x["timestamp"]
                    new_messages += [msg]
                return new_messages

            except Exception as e:
                print('Invalid JSON message', e)
                return []

    def retrieve_all(self) -> list:
        ''' retrieve a list of all messages'''
        # must return a list of DirectMessage objects containing all messages
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((self.server, self.port))
            send = client.makefile("w")
            recv = client.makefile("r")
            try:
                join_msg = f'''{{"join": {{"username": "{self.username}",
                "password": "{self.password}", "token": ""}}}}'''
                send.write(join_msg + '\r\n')
                send.flush()
                resp = reciever(recv)
                start = resp.index("token") + 9
                end = resp.index('"}}')
                token = resp[start:end]
                final = f'{{"token":"{token}", "directmessage": "all"}}'
                send.write(final + '\r\n')
                send.flush()
                response = recv.readline()
                resp = direct_msg(response)
                messages = []
                for x in resp[1]:
                    msg = DirectMessage()
                    msg.recipient = x["from"]
                    msg.message = x["message"]
                    msg.timestamp = x["timestamp"]
                    messages += [msg]
                return messages

            except Exception as e:
                print('Invalid JSON message', e)
                return []
