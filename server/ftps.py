#Lab 3 - ftps.py - Nicholas Bova
from socket import *
import time
import sys
import os
import struct
import select

def change_ACK(ack):
	if ack == 0:
		ack = 1
	else:
		ack = 0
	return ack

#Program global variables below
start_i = 0
end_i = 1000
size_buffer = 1000
tcp_ip = gethostbyname(gethostname()) #DNS name of where ftps.py is
tcp_port = sys.argv[1] #first arg = port number
troll_port = sys.argv[2] #second arg = troll port number
file_size = 0 #to be set when size is recieved from the client
file_name = '' #to bet set when file name is recieved from the client
ACK_bit = 0; #initial ACK bit

#create server socket
server = socket(AF_INET, SOCK_DGRAM)
server.bind((tcp_ip, int(tcp_port)))

#wait for the connection
print ('\nWaiting for packets to be sent...')
# server.listen(1)
# conn, addr = server.accept()
# print ('\nConnected by: '), addr

# loop until it no longer is recieving any data
try:
	while 1:
		data, addr = server.recvfrom(size_buffer) #receiving file size
		file_size = struct.unpack("lhhi", data)
		ack = struct.pack('i', ACK_bit)
		ready = select.select([server],[],[],0.01) #Timeout time of 2 seconds
		while 1:
			if ready[0]:
				data, addr = server.recvfrom(size_buffer)
				break
			else:
				server.sendto(ack, (tcp_ip, int(troll_port)))
				ready = select.select([server],[],[],0.01)				
		server.sendto(data, (tcp_ip, int(troll_port)))
		ACK_bit = change_ACK(ACK_bit)
		break
	#DEBUG CODE
	print ('\nData is being received. Please wait.')
	while 1:
		#server.settimeout(2) #timesout if it no longer recieves data
		data, addr = server.recvfrom(size_buffer) #receiving file name
		file_name = struct.unpack("lhh20s", data)
		ack = struct.pack('i', ACK_bit)
		ready = select.select([server],[],[],0.01) #Timeout time of 2 seconds
		server.sendto(ack, (tcp_ip, int(troll_port)))
		while 1:
			if ready[0]:
				data, addr = server.recvfrom(size_buffer)
				break
			else:
				server.sendto(data, (tcp_ip, int(troll_port)))
				ready = select.select([server],[],[],0.01)
		ACK_bit = change_ACK(ACK_bit)
		break
	#DEBUG CODE
	# print("File size is: " + str(file_size)) #debug code
	decode_name = file_name[3].decode('utf-8', 'ignore')
	decode_name = decode_name.translate(dict.fromkeys(range(32))) #removes any null escape characters that can cause issues with open function
	with open(decode_name, 'bw') as server_file:
		while data: #reads until receives terminating str data
			server.settimeout(10) #timesout if it no longer recieves data
			data, addr = server.recvfrom(size_buffer + 24)
			file_part = struct.unpack("lhh1000s", data)
			data = struct.pack('i', ACK_bit)
			server.sendto(data, (tcp_ip, int(troll_port)))
			ready = select.select([server],[],[],0.15) #Timeout time of 2 seconds
			while 1:
				if ready[0]:
					data, addr = server.recvfrom(size_buffer)
					break
				else:
					server.sendto(data, (tcp_ip, int(troll_port)))	
					ready = select.select([server],[],[],0.01)
			ACK_bit = change_ACK(ACK_bit)
			#copy_file.write(data) #writes 1000 bytes of data to copy_file 			
			server_file.write(file_part[3])
			start_i += size_buffer #increments start_i to move accross bin_file
			end_i += size_buffer
except timeout:
	#clean up
	try:
		server_file.close()
		print("\nTransfer Complete!")
		server.close()
	except NameError:
		print ("Transfer Failed")

