import socket
import threading
import time
import ssl

def Server():
    host = '127.0.0.1'
    #host = '0.0.0.0'
    port = 30000
    s = socket.socket()

    s.bind((host,port))

    s.listen(1)
    c, addr  = s.accept()

    #wrappedSocket = ssl.wrap_socket(c, ssl_version=ssl.PROTOCOL_TLSv1,server_side=True,certfile="C:\cert.pem")
    wrappedSocket = ssl.wrap_socket(c, ssl_version=ssl.PROTOCOL_TLSv1,server_side=True)

    while True:
        data = wrappedSocket.recv(1024)
        if not data:
            break
        print("server received: " + str(data))
        data = str(data).upper()
        print("server sending: " + str(data))
        byte_data = bytearray()
        byte_data.extend(map(ord,data))
        wrappedSocket.send(byte_data)
        #wrappedSocket.send(data)
    wrappedSocket.close()

def Relay():
    time.sleep(0.1)
    host = '127.0.0.1'
    #host = '0.0.0.0'
    port = 30001
    #server_host = '0.0.0.0'
    server_host = '127.0.0.1'
    server_port = 30000

    s2 = socket.socket()
    s2.connect((server_host,server_port))

    s = socket.socket()
    s.bind((host,port))

    s.listen(1)
    c, addr  = s.accept()
    #print "Connection from: " + str(addr)
    while True:
        data = c.recv(1024)
        if not data:
            break

        s2.send(data)

        data = s2.recv(1024)
        #if not data:
        #    break

        c.send(data)

    c.close()
    #s2.close()

def Client():
    time.sleep(0.2)
    host = '127.0.0.1'
    #host = '0.0.0.0'
    port = 30001

    s = socket.socket()
    s.connect((host,port))

    #wrappedSocket = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_TLSv1,ca_certs="cert.pem") 
    wrappedSocket = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_TLSv1) 

    message = input("-> ")
    while message != 'q':
        #wrappedSocket.send(message)
        byte_msg = bytearray()
        byte_msg.extend(map(ord,message))
        wrappedSocket.send(byte_msg)
        data = wrappedSocket.recv(1024)
        print('Received from server: ' + str(data))
        message = input("-> ")
    wrappedSocket.close()


if __name__ == '__main__':

    threads = [
            threading.Thread(target=Server),
            threading.Thread(target=Relay),
            threading.Thread(target=Client),
            ]

    for thread in threads:
        thread.start()



