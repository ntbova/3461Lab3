#Lab 3 - ftpc.py - Nicholas Bova
from socket import *
import time
import sys
import os
import struct
import select

#ip num converter
def ip2l(ip):
    packedIP = inet_aton(ip)
    return struct.unpack("!L", packedIP)[0]
	
#checks the ACK_bit with data and resets ACK_bit accordingly

def change_ACK(ack):
	if ack == 0:
		ack = 1
	else:
		ack = 0
	return ack


#Program global variables below
remote_ip = sys.argv[1] #first arg = remote-IP-on-gamma
remote_port = int(sys.argv[2]) #second arg = remote-port-on-gamma
troll_port = sys.argv[3] #third arg = troll port on beta
strfile = sys.argv[4] #fourth arg = file name
local_ip = gethostbyname(gethostname()) #gets public ip of current server
start_i = 0
end_i = 1000
size_buffer = 1000
ACK_bit = 0; #initial ACK bit
#udp payload segment
#payload = struct.pack('ihh1000s', remote_ip, remote_port, 1)



#creating the client here
client = socket(AF_INET, SOCK_DGRAM)
client.bind((local_ip, 4000)) #CLIENT defaults to port 4000 here
s_local_ip = ip2l(local_ip)#bytes form string to pack into structs
s_strfile = bytes(strfile, 'utf-8')
client.setblocking(0)

#I should probably use the copy.py code from the last lab for this shouldn't I?

#sending the file here
try:
	if os.path.isfile(strfile): #ensures file named "strfile" exists in current directory
		print("File valid. Connecting to troll...")
		file_size = os.path.getsize(strfile)	
		#client.connect((remote_ip, int(remote_port))) #int to convert to integer
		with open(strfile, 'br') as bin_file: #opens pointer of file of binary reader as bin_file
			#first thing to send is the file size
			
			#print("File size is: " + str(file_size)) #debug code
			#client.settimeout(2) #timesout if it no longer recieves data
			size_struct = struct.pack("lhhi", s_local_ip, 4000, 1, file_size) #packing file_size for transfer to server
			client.sendto(size_struct, (local_ip, int(troll_port)))#send the file size first to the troll on troll_port
			ready = select.select([client],[],[],0.05) #Timeout time of 2 seconds
			r_ack = 0;
			while 1:
				if ready[0]:
					data = client.recv(size_buffer)
					r_ack = struct.unpack("i", data)
					if r_ack[0] != ACK_bit:
						client.sendto(size_struct, (local_ip, int(troll_port)))#send the file size first to the troll on troll_port
						ready = select.select([client],[],[],0.05)
					else:
						ACK_bit = change_ACK(ACK_bit)
						break
				else:
					client.sendto(size_struct, (local_ip, int(troll_port)))#send the file size first to the troll on troll_port
					ready = select.select([client],[],[],0.05)
			print(str(r_ack[0]))
			str_struct = struct.pack("lhh20s", s_local_ip, 4000, 2, strfile.encode('utf-8', 'ignore'))
			client.sendto(str_struct, (local_ip, int(troll_port)))#send the file name second
			ready = select.select([client],[],[],2) 
			while 1:
				if ready[0]:
					data = client.recv(size_buffer)
					r_ack = struct.unpack("i", data)
					if r_ack[0] != ACK_bit:
						client.sendto(str_struct, (local_ip, int(troll_port)))#send the file size first to the troll on troll_port
						ready = select.select([client],[],[],0.05)
					else:
						ACK_bit = change_ACK(ACK_bit)
						break
				else:
					client.sendto(str_struct, (local_ip, int(troll_port)))#send the file size first to the troll on troll_port
					ready = select.select([client],[],[],0.05)
			while start_i < file_size: #seek from bin_file until it reaches the end
				bin_file.seek(start_i) #1000 bytes starting at start_i
				data = bin_file.read(end_i - start_i)
				data_struct = struct.pack("lhh1000s", s_local_ip, 4000, 3, data)
				client.sendto(data_struct, (local_ip, int(troll_port)))
				ready = select.select([client],[],[],2) 
				print(str(r_ack[0]))
				while 1:
					if ready[0]:
						data = client.recv(size_buffer)
						r_ack = struct.unpack("i", data)
						if r_ack[0] != ACK_bit:
							client.sendto(data_struct, (local_ip, int(troll_port)))#send the file size first to the troll on troll_port
							ready = select.select([client],[],[],0.05)
						else:
							ACK_bit = change_ACK(ACK_bit)
							break
					else:
						client.sendto(data_struct, (local_ip, int(troll_port)))#send the file size first to the troll on troll_port
						ready = select.select([client],[],[],0.05)
				#copy_file.write(data) #writes 1000 bytes of data to copy_file 
				start_i += size_buffer #increments start_i to move accross bin_file
				end_i += size_buffer
				time.sleep(0.001) #sleep to allow for UDP buffering
			#clean-up after exiting loop
			bin_file.close()
			print("\nFile transfer complete!")
	else: #print error if file not found
		print("File not found.")
except timeout:
	bin_file.close()
#clean-up
client.close()
