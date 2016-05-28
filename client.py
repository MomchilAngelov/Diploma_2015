import socket
import sys
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port_num = int(sys.argv[1])


try:
	while True:

		input_str = input()
		input_str = str.encode(input_str)

		sock.sendto(input_str,('localhost', port_num))
finally:
	sock.close()