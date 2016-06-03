import socket
import sys
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
	while True:
		print("Please input the port: 1 for 12345, anything other number for 12346")
		input_port = input()
		while True:	
			try:
				input_port = int(input_port)
			except ValueError:
				continue
			break

		if input_port == 1:
			input_port = 12345
		else:
			input_port = 12346

		print("Please input the data:")
		input_str = input()
		while True:
			try:
				input_str = str.encode(input_str)
			except ValueError:
				pass
			break

		sock.sendto(input_str,('192.168.97.171', input_port))
finally:
	sock.close()