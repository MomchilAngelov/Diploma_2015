import socket
import sys
import time
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


try:
	while True:

		message = b'ihatemylife'
		sock.sendto(message,('localhost', 12345))
		data = sock.recv(40).decode()
		if data:
			time.sleep(1)
			print("Received data from the server!")

finally:
	sock.close()