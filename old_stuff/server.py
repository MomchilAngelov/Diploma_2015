import socket
import sys
import gameEngine

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_adress = ('localhost', 12346)
sock.bind(server_adress)


all_clients = gameEngine.all_clients_handler()
while True:
	data, addr = sock.recvfrom(40)
	all_clients.check_if_here(addr)
	data = data.decode()

	if data:
		print("{0} received from user {1}".format(data, all_clients.return_user_by_name(addr)))
		print("Sending back data")
		sock.sendto(data.encode(),(addr))
	else:
		break
