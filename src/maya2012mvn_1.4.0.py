import maya.cmds as cmds
import maya.utils as utils
import struct
import socket
import threading
import sys

from struct import *

#TODO
#prints vervangen door sys outs
#ERROR?
#Code executing until print("valid") in transform function
#Neither 'data' not pelvis.tranx are known after a euler message.
#kill.

######################
## GLOBAL VARIABLES 
######################

NAME = None

obarray = []

data = None

# BODY PARTS #
pelvis = None; l5 = None; l3 = None; t12 = None; t8 = None; neck = None; head = None; rish = None
riua = None; rifa = None; riha = None; lesh = None; leua = None; lefa = None; leha = None; 
riul = None; rill = None; rifo = None; rito = None; leul = None; lell = None; lefo = None; leto = None;
# BODY PART NAMES #
bodypart_names = ['_pelvis', '_l5', '_l3', '_t12', '_t8', '_neck', '_head', '_rightshoulder',
                  '_rightupperarm', '_rightforearm', '_righthand', '_leftshoulder', '_leftupperarm', '_leftforearm', '_lefthand',
                  '_rightupperleg', '_rightlowerleg', '_rightfoot', '_righttoe', '_leftupperleg', '_leftlowerleg', '_leftfoot', '_lefttoe']
# STATES #
IDLE = 1
READY_TO_READ = 2
READY_TO_STOP = 3

# DEFAULT STATE #
STATE = IDLE


##########################################################
## USER COMMANDS
## See documentation for the STATE dependency structure 
##########################################################

# FUNCTION: lock()
# lock rig from the scene into the code 
def lock():
	global STATE
		
	if STATE == IDLE:
		STATE = READY_TO_READ
		getName()
		getDetail()
	else:
		return
			
# FUNCTION: unlock()			
# unlock rig 
def unlock():
	global STATE
	
	if STATE == READY_TO_READ:
		dropParts()		#destroy the created objects
		STATE = IDLE
	else:
		return

# FUNCTION: start()
# start transformation process 
def start():
	global STATE
	
	if STATE == READY_TO_READ:
		STATE = READY_TO_STOP
		threading.Thread(target=listen).start()
	else: 
		return

# FUNCTION: stop()
# stop transformation process 
def stop():
	global STATE
	
	if STATE == READY_TO_STOP:
		#kill()
		STATE = READY_TO_READ
	


##############################################
## SUB COMMANDS								
## Functions used by the main user commands 
##############################################

# FUNCTION: getName()
# get the user-input name from the ui after confirm button is pressed
def getName():
    global NAME
    NAME = "pol"
    
# FUNCTION: getDetail()
# create objects for every part of the body for transformation computing
def getDetail():
		global NAME, pelvis, l5, l3, t12, t8, neck, head
		global rish, riua, rifa, riha, lesh, leua, lefa, leha
		global riul, rill, rifo, rito, leul, lell, lefo, leto
		global obarray
		
		pelvis = transformation(); l5 = transformation(); l3 = transformation(); t12 = transformation(); t8 = transformation(); neck = transformation();
		head = transformation(); rish = transformation(); riua = transformation(); rifa = transformation(); riha = transformation();
		lesh = transformation(); leua = transformation(); lefa = transformation(); leha = transformation(); riul = transformation();
		rill = transformation(); rifo = transformation(); rito = transformation(); leul = transformation(); lell = transformation()
		lefo = transformation(); leto = transformation();

		# place in list of objects
		obarray = [pelvis, l5, l3, t12, t8, neck, head, rish, riua, rifa, riha, lesh, leua, lefa, leha, riul, rill, rifo, rito, leul, lell, lefo, leto]

def dropDetail():
		# del pelvis works, but we can not just delete the global vars
		print("Form details dropped.")

# FUNCTION: kill() 	[OUT OF USE]
# interrupt the listen process
def kill():
	global STATE
	if STATE == READY_TO_STOP:
		threading.Thread(target=listen).stop()
	else:
		return

	
# FUNCTION: listen()
# start listening to port which mvn sends to and process incoming data 
# local PORT 5005 set
def listen():
	#the knowledge served by the lock() command in combo with transformation class -- DEBUG LINE
	# UDP CONNECTION DETAILS #
	# set IP + port for the receiver
	UDP_IP = "127.0.0.1"
	UDP_PORT=5005
	# socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	# bind adress to the socket
	sock.bind((UDP_IP, UDP_PORT))
	
	# TRANSFORMATION PROCESSING PART #
	global STATE
	global data
	while STATE == READY_TO_STOP:
		#print("starting to read ..")#DEBUG LINE
		#place received message in data. buffer size is 1024 bytes.
		data, addr = sock.recvfrom(1024)
		transform()
		#utils.executeInMainThreadWithResult(transform)
	
	
# FUNCTION: transform(data)		
# interprets one message and transforms 1 full pose (euler)		
# every data message exsists out of 23 segments	+ 4 extra			
# every segment comes with 28 bytes		
# header is skipped because of validation feature. processing started from index 24
# note: for recording the header part would be neccesary				
def transform():
	global obarray
	global bodypart_names
	global NAME
	global data
	# points to index in the message [data]
	index_pointer = 24
	# points to index in the object array [objectarray]
	array_pointer = 0
	# points to index in the segmentbox array [segmentbox]
	segmentbox_pointer = 0
	# keep track of the float cycles
	cycle_counter = 1
	
	objid = None
	# 4 bytes will be unpacked to one single precision type (float) #
	byte1 = None 
	byte2 = None
	byte3 = None 
	byte4 = None
	# floatcontainer1-6 are xyz translation and xyz rotation #
	fcon1 = None #x tran
	fcon2 = None #y tran
	fcon3 = None #z tran
	fcon4 = None #x rot
	fcon5 = None #y rot
	fcon6 = None #z rot
	#array that holds segment parts
	segmentbox = [objid, fcon1, fcon2, fcon3, fcon4, fcon5, fcon6]
	
	# validate euler message #
	if len(data) == 668:
		#print("valid")
		
		# Beginning of the post-processing round #
		while index_pointer < 668: 
				# object segment ID calculation #
				byte1 = data[index_pointer] #first round 24
				index_pointer += 1
				byte2 = data[index_pointer]
				index_pointer += 1
				byte3 = data[index_pointer]
				index_pointer += 1
				byte4 = data[index_pointer] #first round 27
				index_pointer += 1
				#print(byte1,byte2,byte3,byte4);
				#byte1 = struct.pack('B', byte1)
				#byte2 = struct.pack('B', byte2)
				#byte3 = struct.pack('B', byte3)
				#byte4 = struct.pack('B', byte4)
				
				segmentbox[segmentbox_pointer] = byte1+byte2+byte3+byte4
				#print(byte1,byte2,byte3,byte4);
				segmentbox[segmentbox_pointer] = struct.unpack('>i', segmentbox[segmentbox_pointer])
				#print("Current ID: ", segmentbox[segmentbox_pointer]);

				# place ID in 'item.ID'
				obarray[array_pointer].ID = segmentbox[segmentbox_pointer][0] 
				# point to next part of the segment
				segmentbox_pointer += 1 
				
				# end of segment ID calculation #
				
				# Beginning of the 'float cycles' #
				for cycle in range(6):
				
					#print(index_pointer)
					byte1 = data[index_pointer]
					index_pointer += 1
					byte2 = data[index_pointer]
					index_pointer += 1
					byte3 = data[index_pointer]
					index_pointer += 1
					byte4 = data[index_pointer] 
					index_pointer += 1			
					
					#pack to unsigned bytes
					#byte1 = struct.pack('B', byte1)
					#byte2 = struct.pack('B', byte2)
					#byte3 = struct.pack('B', byte3)
					#byte4 = struct.pack('B', byte4)
					
					#merge into a fcon
					segmentbox[segmentbox_pointer] = byte1+byte2+byte3+byte4
					segmentbox[segmentbox_pointer] = struct.unpack('>f', segmentbox[segmentbox_pointer])
					#print(segmentbox[segmentbox_pointer])
					# python has no switch statement .. #
					if cycle_counter == 1:
						obarray[array_pointer].tranx = segmentbox[segmentbox_pointer][0]
						cycle_counter += 1
					elif cycle_counter == 2:
						obarray[array_pointer].trany = segmentbox[segmentbox_pointer][0]
						cycle_counter += 1
					elif cycle_counter == 3:
						obarray[array_pointer].tranz = segmentbox[segmentbox_pointer][0]
						cycle_counter += 1
					elif cycle_counter == 4:
						obarray[array_pointer].rotx = segmentbox[segmentbox_pointer][0]
						cycle_counter += 1
					elif cycle_counter == 5:
						obarray[array_pointer].roty = segmentbox[segmentbox_pointer][0]
						cycle_counter += 1
					elif cycle_counter == 6:
						obarray[array_pointer].rotz = segmentbox[segmentbox_pointer][0]
						cycle_counter = 1 #reset
					
					# point to next part of the segment
					segmentbox_pointer += 1 
					
				# at the end of the float cycles :
				#print(obarray[array_pointer])
				obarray[array_pointer].trantuple = (obarray[array_pointer].tranx, obarray[array_pointer].trany, obarray[array_pointer].tranz)
				obarray[array_pointer].rotatuple = (obarray[array_pointer].rotx, obarray[array_pointer].roty, obarray[array_pointer].rotz)
				
				# point to next segment for post-processing
				array_pointer += 1
				segmentbox_pointer = 0
		#execute all known transformations
		#print("obarray before attribute setting", obarray)
		utils.executeInMainThreadWithResult(execute_transformations)				
	else:
		#print("invalid")
		stop()
		
def execute_transformations():
	for i in range(len(bodypart_names)):
			cmds.setAttr(NAME + bodypart_names[i] + '.translate', obarray[i].trantuple[0], obarray[i].trantuple[1], obarray[i].trantuple[2])
			cmds.setAttr(NAME + bodypart_names[i] + '.rotate', obarray[i].rotatuple[0], obarray[i].rotatuple[1], obarray[i].rotatuple[2])

	
	
#############	
## CLASSES 
#############

class transformation:
				trantuple = None
				rotatuple = None 
				
				#translation and rotation variables
				tranx = None
				trany = None
				tranz = None
					
				rotx = None
				roty = None
				rotz = None
					
				ID = None
