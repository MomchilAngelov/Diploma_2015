import socket
import sys
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
	while True:
		print("Please input the port: 1 for 12345, anything other number for 12346")
		input_port = input()
		input_port = int(input_port)
		if input_port == 1:
			input_port = 12345
		else:
			input_port = 12346

		print("Please input the data:")
		input_str = input()
		input_str = str.encode(input_str)

		sock.sendto(input_str,('localhost', input_port))
finally:
	sock.close()