#Lab 2 - ftps.py - Nicholas Bova
import socket
import sys
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
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((tcp_ip, int(tcp_port)))

#wait for the connection
print ('\nWaiting for packets to be sent...')
# server.listen(1)
# conn, addr = server.accept()
# print ('\nConnected by: '), addr

# loop until it no longer is recieving any data
while 1:
	data, addr = server.recvfrom(4) #receiving file size
	file_size = struct.unpack("i", data)
	server.sendto(data, addr) 
	break
#DEBUG CODE
print (file_size)
while 1:
	data, addr = server.recvfrom(20) #receiving file name
	file_name = data.decode()
	server.sendto(data, addr)
	break
#DEBUG CODE
print (file_name)
# print("File size is: " + str(file_size)) #debug code

with open(file_name, 'bw') as server_file:
	while type(data[3]) != 'i': #reads until receives terminating str data
		data, addr = server.recvfrom(size_buffer)
		#copy_file.write(data) #writes 1000 bytes of data to copy_file 			
		server_file.write(data[3])
		start_i += size_buffer #increments start_i to move accross bin_file
		end_i += size_buffer	
	server_file.close()
# conn.sendall(data)
#clean up
print("\nTransfer Complete!")
server.close()
conn.close()
