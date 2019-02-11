import socket
import threading
import time
import ssl

CURRENT_STUDENT = "Talley_Amir"

cert_file = "certfiles/" + CURRENT_STUDENT + "_cert.pem"
pdf_file = "Submitted-Files/" + CURRENT_STUDENT + "_submission.pdf"

#host = socket.gethostbyname("jaguar.cs.yale.edu")
#(host,x,y) = socket.gethostbyaddr("172.27.202.55")
host = "127.27.202.55"
print(host)
port = 3001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("about to connect...")
s.connect((host,port))
print("connected")


wrappedSocket = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_TLSv1,ca_certs=cert_file) 
#wrappedSocket = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_TLSv1) 

f = open(pdf_file,'wb')
print("opened file")
#message = f.read(1024)
while True:
    data = wrappedSocket.recv(1024)
    message = f.write(data)
    if not data:
        break
wrappedSocket.close()
print('reached here')
