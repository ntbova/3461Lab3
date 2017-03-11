#Lab 2 - ftps.py - Nicholas Bova
from socket import *
import sys
import select
import os
import struct

#Program global variables below
start_i = 0
end_i = 1000
size_buffer = 1000
tcp_ip = '' #DNS name of where ftps.py is
tcp_port = sys.argv[1] #first arg = port number
file_size = 0 #to be set when size is recieved from the client
file_name = '' #to bet set when file name is recieved from the client

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
		server.settimeout(2) #timesout if it no longer recieves data
		data, addr = server.recvfrom(size_buffer) #receiving file size
		file_size = struct.unpack("lhhi", data)
		server.sendto(data, addr) 
		break
	#DEBUG CODE
	print ('\nData is being received. Please wait.')
	while 1:
		server.settimeout(2) #timesout if it no longer recieves data
		data, addr = server.recvfrom(size_buffer) #receiving file name
		file_name = struct.unpack("lhh20s", data)
		server.sendto(data, addr)
		break
	#DEBUG CODE
	# print("File size is: " + str(file_size)) #debug code
	decode_name = file_name[3].decode('utf-8', 'ignore')
	decode_name = decode_name.translate(dict.fromkeys(range(32))) #removes any null escape characters that can cause issues with open function
	null_string = "\x00" * 1000
	with open(decode_name, 'bw') as server_file:
		while data: #reads until receives terminating str data
			server.settimeout(2) #timesout if it no longer recieves data
			data, addr = server.recvfrom(size_buffer + 24)
			file_part = struct.unpack("lhh1000s", data)
			#copy_file.write(data) #writes 1000 bytes of data to copy_file 			
			server_file.write(file_part[3])
			start_i += size_buffer #increments start_i to move accross bin_file
			end_i += size_buffer
except timeout:
	#clean up
	server_file.close()
	print("\nTransfer Complete!")
	server.close()

