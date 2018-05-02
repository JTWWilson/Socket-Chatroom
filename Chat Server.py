import socket
import threading
import json

print(socket.gethostname())
HOST = socket.gethostname()#'10.0.77.177' #'10.0.216.136'
PORT = 9999

messages = []


def listener(s):
    """
    Listens to given socket 'sock' and prints any data received
    :param sock: socket to listen to
    """
    while True:
        data = s.recv(1024)
        if data:
            messages.append(json.loads(data.decode()))
        print('received:', json.loads(data.decode()))


class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        thread_no = 0
        while True:
            client, address = self.sock.accept()
            print('Client attached on {}'.format(address))
           # client.send('Got client'.encode('ascii'))
            client.settimeout(600)
            threading.Thread(target = listener, args = (client,)).start()
            thread_no += 1
            threading.Thread(target = self.manage_client,args = (client, address, thread_no)).start()

    def manage_client(self, client, address, thread_num):
        size = 1024
        sent_messages = len(messages)
        while True:
            #print(thread_num)

            #data = client.recv(size)
            ##print('received: {}'.format(json.loads(data.decode())))
            #if data:
            #    unpacked_data = json.loads(data.decode())
            #    sent_messages += 1
            #    messages.append(unpacked_data)
            #    print(messages)
            #else:
            #    raise Exception('Client disconnected')
            #print(thread_num, ': ', sent_messages, messages)
            if sent_messages < len(messages):
                print('sending {}'.format(messages[-1]))
                sent_messages += 1
                client.send(json.dumps(messages[-1]).encode())

if __name__ == "__main__":
    ThreadedServer(HOST, PORT).listen()
