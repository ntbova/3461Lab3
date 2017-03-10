#Lab 2 - ftpc.py - Nicholas Bova
import socket
import sys
import os
import struct

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
	file_size = os.path.getsize(strfile)	
	client.connect((remote_ip, int(remote_port))) #int to convert to integer
	with open(strfile, 'br') as bin_file: #opens pointer of file of binary reader as bin_file
		#first thing to send is the file size
		
		#print("File size is: " + str(file_size)) #debug code
		size_struct = struct.pack("i", file_size) #packing file_size for transfer to server
		client.send(size_struct)#send the file size first
		data = client.recv(size_buffer) #wait to get data sent back from server for confirmation
		client.send(strfile.encode())#send the file name second
		data = client.recv(size_buffer)
		while start_i < file_size: #seek from bin_file until it reaches the end
			bin_file.seek(start_i) #1000 bytes starting at start_i
			data = bin_file.read(end_i - start_i)
			client.sendall(data)
			#copy_file.write(data) #writes 1000 bytes of data to copy_file 
			start_i += size_buffer #increments start_i to move accross bin_file
			end_i += size_buffer
		#clean-up after exiting loop
		bin_file.close()
		print("\nFile transfer complete!")
else: #print error if file not found
	print("File not found.")
#clean-up
client.close()
