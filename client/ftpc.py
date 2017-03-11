#Lab 2 - ftpc.py - Nicholas Bova
import socket
import time
import sys
import os
import struct

#Program global variables below
remote_ip = sys.argv[1] #first arg = remote-IP-on-gamma
remote_port = int(sys.argv[2]) #second arg = remote-port-on-gamma
troll_port = sys.argv[3] #third arg = troll port on beta
strfile = sys.argv[4] #fourth arg = file name
local_ip = socket.gethostbyname(socket.gethostname()) #gets public ip of current server
start_i = 0
end_i = 1000
size_buffer = 1000

#udp payload segment
#payload = struct.pack('ihh1000s', remote_ip, remote_port, 1)

#creating the client here
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind((local_ip, 4000))
s_local_ip = bytes(local_ip, 'utf-8') #bytes form string to pack into structs
s_strfile = bytes(strfile, 'utf-8')

#I should probably use the copy.py code from the last lab for this shouldn't I?

#sending the file here
if os.path.isfile(strfile): #ensures file named "strfile" exists in current directory
	print("File valid. Connecting to troll...")
	file_size = os.path.getsize(strfile)	
	#client.connect((remote_ip, int(remote_port))) #int to convert to integer
	with open(strfile, 'br') as bin_file: #opens pointer of file of binary reader as bin_file
		#first thing to send is the file size
		
		#print("File size is: " + str(file_size)) #debug code

		size_struct = struct.pack("4shhi", s_local_ip, 4000, 1, file_size) #packing file_size for transfer to server
		client.sendto(size_struct, (local_ip, int(troll_port)))#send the file size first to the troll on troll_port
		data = client.recv(size_buffer) #wait to get data sent back from server for confirmation
		str_struct = struct.pack("4shh20s", s_local_ip, 4000, 2, s_strfile)
		client.sendto(str_struct, (local_ip, int(troll_port)))#send the file name second
		data = client.recv(size_buffer)
		while start_i < file_size: #seek from bin_file until it reaches the end
			bin_file.seek(start_i) #1000 bytes starting at start_i
			data = bin_file.read(end_i - start_i)
			data_struct = struct.pack("4shh1000s", s_local_ip, 4000, 3, data)
			client.sendto(data_struct, (local_ip, int(troll_port)))
			#copy_file.write(data) #writes 1000 bytes of data to copy_file 
			start_i += size_buffer #increments start_i to move accross bin_file
			end_i += size_buffer
			time.sleep(0.001) #sleep to allow for UDP buffering
		#clean-up after exiting loop
		bin_file.close()
		print("\nFile transfer complete!")
else: #print error if file not found
	print("File not found.")
#clean-up
# end_struct = struct.pack("4shhi", s_local_ip, 4000, 1, 0)
# client.sendto(end_struct, (local_ip, int(troll_port)))
client.close()
