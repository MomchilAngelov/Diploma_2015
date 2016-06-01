import socket
import sys
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
	while True:
		print("Please input the port:")
		input_port = input()
		input_port = int(input_port)

		print("Please input the data:")
		input_str = input()
		input_str = str.encode(input_str)

		sock.sendto(input_str,('localhost', input_port))
finally:
	sock.close()