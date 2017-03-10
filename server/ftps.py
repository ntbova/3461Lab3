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
print ('\nWaiting for client to connect.')
server.listen(1)
conn, addr = server.accept()
#print ('\nConnected by: '), addr

#loop until it no longer is recieving any data
#while 1:
data = conn.recv(4)
file_size = struct.unpack("i", data)
conn.send(data)
#if not data: break
#check what kind of data it is by the size
#if sys.getsizeof(data) == 4:
#if sys.getsizeof(data) == 20:
#else:
#file_size = int(data.decode())
data = conn.recv(20) #recieving file name
conn.send(data) #send back to confirm
file_name = data.decode()

print("File size is: " + str(file_size)) #debug code

with open(file_name, 'bw') as server_file:
	while data: #reads until it is no longer recieving data
			
		data = conn.recv(size_buffer)
		#copy_file.write(data) #writes 1000 bytes of data to copy_file 			
		server_file.write(data)
		start_i += size_buffer #increments start_i to move accross bin_file
		end_i += size_buffer	
	server_file.close()
conn.sendall(data)
#clean up
print("\nTransfer Complete!")
server.close()
conn.close()
