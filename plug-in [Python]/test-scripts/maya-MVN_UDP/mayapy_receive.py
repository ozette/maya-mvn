#T.13 - 47
#Python to Maya script test

# establish library for udp connection
import socket

counter = 0

#set IP + port for the receiver
UDP_IP="127.0.0.1"
UDP_PORT=5005

sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )

#bind receiver to the adress
sock.bind( (UDP_IP,UDP_PORT) )

#while true read. buffer size is 1024 bytes. message is set in data.
while True:
    print('starting to read..')
    data, addr = sock.recvfrom(1024)
    print("received message:", data)
    if data != 0:
        counter += 1
        print("bytes received:", len(data))
        print(counter)
        
        

print(counter)
        
    
