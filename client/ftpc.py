import socket
import sys
import os

#Program global variables below
remote_ip = sys.argv[1] #first arg = remote-IP-on-gamma
remote_port = sys.argv[2] #second arg = remote-port-on-gamma
strfile = sys.argv[3] #third arg = file name
start_i = 0
end_i = 1000
size_buffer = 1000

#creating the client here
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#I should probably use the copy.py code from the last lab for this shouldn't I?

#sending the file here
if os.path.isfile(strfile): #ensures file named "strfile" exists in current directory
	print("File valid. Connecting to server...")	
	client.connect((remote_ip, int(remote_port))) #int to convert to integer
	with open(strfile, 'br') as bin_file: #opens pointer of file of binary reader as bin_file
		#first thing to send is the file size
		file_size = os.path.getsize(strfile)
		client.sendall(file_size)#send the file size first
		client.sendall(strfile)#send the file name second
		while start_i < bin_size: #seek from bin_file until it reaches the end
			bin_file.seek(start_i) #1000 bytes starting at start_i
			data = bin_file.read(end_i - start_i)

			client.sendall(data)
			#copy_file.write(data) #writes 1000 bytes of data to copy_file 


			start_i += byte_size #increments start_i to move accross bin_file
			end_i += byte_size
		#clean-up after exiting loop
		bin_file.close()
		copy_file.close()
else: #print error if file not found
	print("File not found.")
