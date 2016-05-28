class socketHandler(threaing.Thread, socket with address):
	socket
	address
	__init__:
		self.socket = socket
		self.address = adrress
	run:
		socket.send("Am i connected")
		

while 1:
	conn, addr = s.accept()
	client = socketHandler(conn, addr)
	client.start()
