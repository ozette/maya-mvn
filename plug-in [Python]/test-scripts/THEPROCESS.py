#THE PROCESS#

import struct

#purpose, save transformation values until execution process
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
				
pelvis = transformation(); l5 = transformation(); l3 = transformation(); t12 = transformation(); t8 = transformation(); neck = transformation();
head = transformation(); rish = transformation(); riua = transformation(); rifa = transformation(); riha = transformation();
lesh = transformation(); leua = transformation(); lefa = transformation(); leha = transformation(); riul = transformation();
rill = transformation(); rifo = transformation(); rito = transformation(); leul = transformation(); lell = transformation()
lefo = transformation(); leto = transformation();

obarray = [pelvis, l5, l3, t12, t8, neck, head, rish, riua, rifa, riha, lesh, leua, lefa, leha, riul, rill, rifo, rito, leul, lell, lefo, leto]

def transform(data):
	global obarray
	
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
		print("valid")
		
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
				
				byte1 = struct.pack('B', byte1)
				byte2 = struct.pack('B', byte2)
				byte3 = struct.pack('B', byte3)
				byte4 = struct.pack('B', byte4)
				
				segmentbox[segmentbox_pointer] = byte1+byte2+byte3+byte4
				segmentbox[segmentbox_pointer] = struct.unpack('>i', segmentbox[segmentbox_pointer])
				
				print('id is ', segmentbox[segmentbox_pointer][0])

				# place ID in 'item.ID'
				obarray[array_pointer].ID = segmentbox[segmentbox_pointer][0] 
				# point to next part of the segment
				segmentbox_pointer += 1 
				
				# end of segment ID calculation #
				
				# Beginning of the 'float cycles' #
				for cycle in range(6):
				
					byte1 = data[index_pointer]
					index_pointer += 1
					byte2 = data[index_pointer]
					index_pointer += 1
					byte3 = data[index_pointer]
					index_pointer += 1
					byte4 = data[index_pointer] 
					index_pointer += 1			
					
					#pack to unsigned bytes
					byte1 = struct.pack('B', byte1)
					byte2 = struct.pack('B', byte2)
					byte3 = struct.pack('B', byte3)
					byte4 = struct.pack('B', byte4)
					
					#merge into a fcon
					segmentbox[segmentbox_pointer] = byte1+byte2+byte3+byte4
					segmentbox[segmentbox_pointer] = struct.unpack('>f', segmentbox[segmentbox_pointer])
					
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
				obarray[array_pointer].trantuple = (obarray[array_pointer].tranx, obarray[array_pointer].trany, obarray[array_pointer].tranz)
				print(obarray[array_pointer].trantuple)
				obarray[array_pointer].rotatuple = (obarray[array_pointer].rotx, obarray[array_pointer].roty, obarray[array_pointer].rotz)
				print(obarray[array_pointer].rotatuple)
				
				# point to next segment for post-processing
				array_pointer += 1
				segmentbox_pointer = 0
				print('indexpointer is', index_pointer)
		#execute all known transformations
	else:
		print("invalid")
		stop()
		
	#print(data) #DEBUG LINE
	
	

				
