#T.13 - 47
#Python to Maya script test

# establish library for udp connection.
import socket

# assign cmds to be intepreted as maya commands. [NOT IMPLEMENTED YET]
# import maya.cmds as cmds

#set targets and a test message
UDP_IP="127.0.0.1"
UDP_PORT=5005
MESSAGE= 'Test message'

#print target values and test message
print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)

#declare open socket (Internet + UDP)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#send message to target IP + port (string is casted to bytes in Python 3.x)
sock.sendto( (bytes(MESSAGE, 'UTF-8')), (UDP_IP,UDP_PORT) )
