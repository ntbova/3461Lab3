import socket
import sys
import os

#Program global variables below
start_i = 0
end_i = 1000
size_buffer = 1000
tcp_ip = '' #DNS name of where ftps.py is
tcp_port = 5000 #ftp port num
file_size = 0 #to be set when size is recieved from the client
file_name = '' #to bet set when file name is recieved from the client

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((tcp_ip, tcp_port))

#wait for the connection
print '\nWaiting for client to connect.'
server.listen(1)
conn, addr = server.accept()
print '\nConnected by', addr

#loop until it no longer is recieving any data
while 1:
	data = conn.recv(size_buffer)	
	if not data: break
	#check what kind of data it is by the size
	if sys.getsizeof(data) == 4:
		file_size = data
	if sys.getsizeof(data) == 20:
		file_name = data
	else:
		with open(file_name, 'bw') as server_file:
			while start_i < file_size: #seek from bin_file until it reaches the end
			
				data = conn.recv(size_buffer)
				#copy_file.write(data) #writes 1000 bytes of data to copy_file 			
				server_file.write(data)

				start_i += byte_size #increments start_i to move accross bin_file
				end_i += byte_size
		
	
	conn.sendall(data)
#clean up
server.close()
conn.close()
